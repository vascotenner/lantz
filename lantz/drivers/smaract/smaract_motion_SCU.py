# -*- coding: utf-8 -*-
"""
    lantz.drivers.newport.motion axis
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    General class that implements the commands used for several smaract motion
    drivers using the ASCII mode (via serial or serial via USB).

    :copyright: 2018, see AUTHORS for more details.
    :license: GPL, see LICENSE for more details.

    Source: Instruction Manual (Smaract)

"""


from lantz.feat import Feat
from lantz.action import Action
from lantz.messagebased import MessageBasedDriver, _PARSERS_CACHE
from lantz.processors import ParseProcessor
from lantz.driver import unit_replace
from pyvisa import constants
from lantz import Q_
from lantz.drivers.motion import MotionAxisMultiple, MotionControllerMultiAxis, BacklashMixing
import time
import numpy as np

_ERRORS = {0: ("No error Indicates that no error occurred and therefore corresponds to an acknowledge."),
1: ("Parse error", "The command could not be processed due to a parse error.  "),
2: ("Unknown command error", "The command given is not known to the system.  "),
3: ("Invalid channel error", "The channel index given is invalid and the command cannot be processed."),
4: ("Invalid mode error", "The parameter that defines the mode for automatic error reporting is not valid, such that the mode change cannot be processed.  "),
13: ("Syntax error", "The command could not be processed due to a syntax error."),
15: ("Overflow error", "A number value given was too large to be processed.  "),
17: ("Invalid parameter error", "A parameter that was given with the command was invalid."),
18: ("Missing parameter error", "A parameter was omitted where it was required.  "),
19: ("No Sensor Present Error", "This error occurs if a command was given that requires sensor feedback, but the addressed positioner has none attached.  "),
20: ("Wrong Positioner Type Error", "Some commands are only executable for certain positioner types. For example, issuing an MAA command to a linear positioner leads to this error."),
21: ("End Stop Reached Error", "This error occurs if the last closed-loop movement command of a channel was aborted due to end stop detection. Reporting of this error can be enabled or disabled for each channel."),
22: ("Targeting Timeout Error", "This error occurs if the last closed-loop movement command of a channel was aborted due to not terminating after a fixed timeout. Reporting of this error can be enabled or disabled for each channel."),
23: ("HV Range Error", "If the voltage operating the positioners is out of range, all movement will be stopped and only a power cycle sets the device back into operating mode. This may be caused e.g. by defective cabling."),
24: ("Temperature Overheat Error", "If a system becomes too hot for any reason, all movement is stopped. Furthermore the operating mode is paused and automatically resumed when the system has cooled down."),
25: ("Calibration Failed Error", "This error occurs if the last calibration command of a channel was aborted due to a mechanically blocked positioner. Note that this might as well be the case when calibrating near an end stop."),
26: ("Referencing Failed Error", "This error occurs if the last move-to-reference command of a channel was aborted. If this happens, the system has not been able to detect the desired mark(s). A possible reason might be an incorrect positioner type setting."),
27: ("Not Processable Error", "The given command cannot be processed (at the moment). This might occur when issuing a SZ – Set Zero command while the positioner is still moving."),
}

_MOVEMENT_STATUS = {'S': 'Stopped',
                    'A': 'Amplitude setting',
                    'M': 'Moving',
                    'T': 'Targeting',
                    'H': 'Holding',
                    'C': 'Calibrating',
                    'R': 'Referencing',
                    }


_POSITIONERS_ROTATION = {29: {'comment': '25.4 mm tip-tilt mirror mount axis, inductive sensor with 73 µ° resolution',
                              'reference': 'end stop',
                              'series': 'STxxxxS1I1E2',
                              'units': 'millidegree'}
                         }
_POSITIONERS_TRANSLATION = {}

class SCU(MessageBasedDriver, MotionControllerMultiAxis):
    """ Driver for SCU controller with multiple axis

    """
    DEFAULTS = {
                'COMMON': {'write_termination': '\n',
                           'read_termination': '\n', },
                'ASRL': {
                    'timeout': 100,  # ms
                    'encoding': 'ascii',
                    'data_bits': 8,
                    'baud_rate': 9600,
                    'parity': constants.Parity.none,
                    'stop_bits': constants.StopBits.one,
                    #'flow_control': constants.VI_ASRL_FLOW_NONE,
                    'flow_control': constants.VI_ASRL_FLOW_XON_XOFF,  # constants.VI_ASRL_FLOW_NONE,
                    },
                }

    def __init__(self, resource_name, name=None, **kwargs):
        super().__init__(resource_name, name=None, **kwargs)
        self._parseprocessor_error = ParseProcessor(':E{:i}')

    def initialize(self):
        super().initialize()

        # Set Errormode to directly return errorsL
        MessageBasedDriver.write(self, ':E1')
        MessageBasedDriver.read(self)

        self.detect_axis()

    def query(self, command, *, send_args=(None, None), recv_args=(None, None)):
        return self.write(command, send_args=send_args, recv_args=recv_args)

    def write(self, command, *, send_args=(None, None), recv_args=(None, None)):
        MessageBasedDriver.write(self, ':{}'.format(command), *send_args)
        ret = self.read(*recv_args)

        # check for errors:
        try:
            err = int(self._parseprocessor_error(ret))
            if err == 0:
                raise ValueError('No error')
            self.log_error('Writing command: {} gave error: {} ({})', command, *_ERRORS[err])
        except ValueError:
            return ret

    @Feat()
    def idn(self):
        return self.parse_query('I', format=':I{:s}')

    @Action()
    def detect_axis(self):
        """ Find the number of axis available.

        The detection stops as soon as an empty controller is found.
        """
        num = 0
        while True:
            axis = MotionAxis(parent=self, num=num,
                          id='{}.axis[{}]'.format(self.idn, num))
            if not axis.present:
                return

            self.axes.append(axis)

            # update units of axis NOT WORKING on 20190109
            #axis.update({'units': {**_POSITIONERS_ROTATION, **_POSITIONERS_TRANSLATION}[axis.type]['units']},
            #            force=True)

            num += 1


class MotionAxis(MotionAxisMultiple):
    def __init__(self, parent, num, id, *args, **kwargs):
        newconfig = kwargs.pop('config', {})
        if 'default_hold_time' not in newconfig:
            newconfig['default_hold_time'] = 60000  # infinity
        if 'accuracy' not in newconfig:
            newconfig['accuracy'] = 0.057
        kwargs['config'] = newconfig

        super().__init__(parent, num, id, *args, **kwargs)

    def __del__(self):
        self.parent = None
        self.num = None

    def query(self, command, *, send_args=(None, None), recv_args=(None, None)):
        base_command = '{}{:d}'.format(command, self.num)
        return self.parent.query(base_command,
                                 send_args=send_args, recv_args=recv_args,
                                       )

    def query_get(self, command, *, send_args=(None, None), recv_args=(None, None)):
        """Query specific for get commands: the G is prepended automatically."""
        base_command = '{}{:d}'.format(command, self.num)
        return self.parent.parse_query('G' + base_command,
                                 send_args=send_args, recv_args=recv_args,
                                       format=':' + base_command + '{:s}')

    def parse_query_get(self, command, *,
                    send_args=(None, None), recv_args=(None, None),
                    format=None):
        """Send query to the instrument, parse the output using format
        and return the answer.

        .. seealso:: TextualMixin.query and stringparser
        """
        ans = self.query_get(command, send_args=send_args, recv_args=recv_args)
        if format:
            parser = _PARSERS_CACHE.setdefault(format, ParseProcessor(format))
            ans = parser(ans)
        return ans

    def write(self, command, *args, **kwargs):
        return self.parent.write('{}{:d}'.format(command, self.num,),
                                 *args, **kwargs)

    @Feat()
    def idn(self):
        return self.num

    @Feat(values={True: 'P', False: 'N'})
    def present(self):
        return self.query_get('SP')

    @Feat(read_once=True)
    def type(self):
        ret = int(self.parse_query_get('ST', format='T{:i}'))
        if ret not in {**_POSITIONERS_ROTATION, **_POSITIONERS_TRANSLATION}:
            self.log_error('Positioner with unknown type {}. Look in manual for more information', ret)
        return ret


    @Action()
    def define_home(self):
        """Remap current position to home (0)"""
        self.write('SZ')

    @Action()
    def calibrate_sensor(self):
        """Calibrate sensor

        Make sure that position is not close to end stop
        """
        self.write('CS')

    @Feat(units='ms')
    def default_hold_time(self):
        return self._config['default_hold_time']

    @default_hold_time.setter
    def default_hold_time(self, val):
        self._config['default_hold_time'] = val

    @Feat(units='millidegree')
    def position(self):
        if self.type in _POSITIONERS_ROTATION:
            return self.parse_query_get('A', format='A{}R{}')[0]
        if self.type in _POSITIONERS_TRANSLATION:
            return self.parse_query_get('P', format='P{}')

    @position.setter
    def position(self, pos):
        """
        Waits until movement is done if self._config['wait_until_done'] = True.

        :param pos: new position
        """
        self._set_position(pos, wait=self._config['wait_until_done'])


    @Action(units=['millidegree', None, 'ms'])
    def _set_position(self, pos, wait=None, hold_time=-1*Q_('ms')):
        """
        Move to an absolute position, taking into account backlash.

        When self.backlash is to a negative value the stage will always move
         from low to high values. If necessary, a extra step with length
         self.backlash is set.

        :param pos: New position in mm
        :param wait: wait until stage is finished
        :param hold_time: Time how long the stage should hold to the set position
        """

        # First do move to extra position if necessary

        if hold_time == -1:
            hold_time = self.default_hold_time.m

        self.__set_position(pos, hold_time=hold_time)
        if wait:
            self._wait_until_done()
            self.check_position(pos)

    def __set_position(self, pos, hold_time):
        """
        Move stage to a certain position
        :param pos: New position
        :param hold_time:
        """

        if self.type in _POSITIONERS_ROTATION:
            self.parent.write('MAA{}A{}H{}'.format(self.num, (pos), int(hold_time)))
        if self.type in _POSITIONERS_TRANSLATION:
            raise NotImplemented

        self.last_set_position = pos

    @Action(units='millidegree')
    def check_position(self, pos):
        '''Check is stage is at expected position CAN BE REMOVED as change_units is working'''
        if np.isclose(self.position.m, pos, atol=self.accuracy.m):
            return True
        self.log_error('Position accuracy {} is not reached.'
                       'Expected: {}, measured: {}'.format(self.accuracy,
                                                           pos,
                                                           self.position))
        return False
    @Action()
    def stop(self):
        """Emergency stop"""
        self.write('S')

    @Feat()
    def motion_status(self):
        ret = self.query('M')
        return ret[-1]

    @Feat()
    def motion_done(self):
        if self.motion_status in ['H', 'S']:
            return True
        return False
