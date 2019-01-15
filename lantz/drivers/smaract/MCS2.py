# -*- coding: utf-8 -*-
"""
    lantz.drivers.smaract.smaract.MCS2 axis
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    General class that implements the commands used for several smaract motion
    drivers using MCS2 dll

    :copyright: 2018, see AUTHORS for more details.
    :license: GPL, see LICENSE for more details.

    Source: Instruction Manual (Smaract)

"""

import ctypes as ct
from ctypes import c_uint, c_int, byref
from lantz.errors import InstrumentError
from lantz.foreign import LibraryDriver
from lantz.feat import Feat
from lantz.action import Action

from lantz import Q_, ureg
from lantz.processors import convert_to
from lantz.drivers.motion import MotionAxisMultiple, MotionControllerMultiAxis, BacklashMixing
import time
import numpy as np

import lantz.drivers.smaract.SmarActControlConstants as SmarActControlConstants

# Generate dict of error codes from altered header file
_ERRORS = {getattr(SmarActControlConstants, constant): constant[13:]
           for constant in dir(SmarActControlConstants)
           if constant[:13] == 'SA_CTL_ERROR_'}

# List of functions that should not be checked for errorcodes
_IGNORE_ERR = []

SA_CTL_DeviceHandle_t = ct.c_uint32
SA_CTL_TransmitHandle_t = ct.c_uint32
SA_CTL_StreamHandle_t = ct.c_uint32

SA_CTL_RequestID_t = ct.c_uint8
SA_CTL_PropertyKey_t = ct.c_uint32
SA_CTL_Result_t = ct.c_uint32

class MCS2_Find_devices(LibraryDriver):
    """ Driver for MCS controller

    """
    LIBRARY_NAME = 'smaractctl'

    def _add_types(self):
        self.lib.SA_CTL_FindDevices.argtypes = [ct.c_char_p, ct.c_char_p, ct.POINTER(ct.c_size_t)]
        self.lib.SA_CTL_Open.argtypes = [ct.POINTER(SA_CTL_DeviceHandle_t), ct.c_char_p, ct.c_char_p]
        pass
        # self.lib.XC_OpenCamera.argtypes = [ct.c_uint]

    def _return_handler(self, func_name, ret_value):
        if self.lib.__getattribute__(func_name).restype != ct.c_void_p and (func_name not in _IGNORE_ERR):
            if ret_value > 0:
                try:
                    message = _ERRORS[ret_value]
                except KeyError:
                    message = 'Errorcode {}. Please lookup in manual page 266'.format(ret_value)
                raise InstrumentError(message)

    @Action()
    def find_devices(self):
        raise NotImplementedError
        #deviceList = (ct.c_char_p * 1000)()
        #ioDeviceListLen = len(deviceList)
        deviceList = ""
        ioDeviceListLen = ct.c_size_t(len(deviceList))
        self.lib.SA_CTL_FindDevices("", deviceList, byref(ioDeviceListLen))

class MCS2_Bare(MCS2_Find_devices):
    def __init__(self, device_locator=None, *args, **kwargs):
        """ Set default settings for device

        :param device_locator: string, eg:
                'usb:sn:<serial>'
                'usb:ix:<n>'
                'network:sn:<serial>'
                'network:<ip>'
        """


        super().__init__(*args, **kwargs)
        self.device_locator = device_locator
        self.dHandle = ct.c_uint32()
        self.dll = self.lib
        self.num_of_chan = None

    def initialize(self):
        """
        Initialize the piezo stage
        context will be passed to self.dHandle
        """
        self.lib.SA_CTL_Open(byref(self.dHandle), self.device_locator, "");
#        self.lib.SA_OpenSystem(byref(self.dHandle), self.device_locator, 'sync')

    def finalize(self):
        self.lib.SA_CTL_Close(self.dHandle)

#TODO
class TODO():
    def setchannelproperty(self, channel_idx, selector, subselector, prop, propvalue):
        """
        SetChannelProperty(self, channel_idx, selector, subselector, prop, propvalue):
        sets channel properties to different values

        Args:
            channel_idx(int): choose a channel(each corresponds a linear translation axis of a stage or a rotational axis)
            selector(int): broad category
            subselector(int):narrower category
            prop(int):property to change
            propvalue(int): value to change it too

            here are some of the more usefull properties to change and corresponding subselectors

            selector 1:general
                subselector 2:Low Vibration mode
                    prop 1:Operation mode
                        propvalues 0,1:enabled,disabled




        """

        self.dll.SA_SetChannelProperty_S(self.MCS_HANDLE, channel_idx, self.dll.SA_EPK(selector, subselector, prop), propvalue)

    def get_number_of_channels(self):
        """"
        saves the number of detected channels


        """
        NUMOFCHANNELS = c_uint()
        error = self.dll.SA_GetNumberOfChannels(self.MCS_HANDLE, byref(NUMOFCHANNELS))
        self.num_of_chan = NUMOFCHANNELS.value
        return NUMOFCHANNELS

    def go_to_angle(self,channel_idx,angle,revolution,holdtime):
        """

        :param channel_idx: channel to rotate
        :param angle: angle to move to in micro radians, if the sensor is on( change with set_power_mode(channel_idx,mode)
                        stored in self.power_mode), will be interpreted as a move to a certain angle compared to the
                        current zero point if the sensor power_mode is disabled it will rotate with respect
                        to the current angle
        :param revolution: number of 360 degree revolutions
        :param holdtime:
        :return:
        """

        if self.power_mode==0:
            self.dll.SA_gotoAngleRelative_S(self.MCS_HANDLE,channel_idx,c_uint(angle),c_int(revolution),c_int(holdtime))
        else:
            self.dll.SA_GotoAngleAbsolute_S(self.MCS_HANDLE,channel_idx,c_uint(angle),c_int(revolution),c_int(holdtime))

    def rotate_relative(self, channel_idx, angle,revolution, holdtime):
        self.dll.SA_gotoAngleRelative_S(self.MCS_HANDLE, channel_idx, c_uint(angle), c_int(revolution), c_int(holdtime))

    def set_power_mode(self,mode):
        """
        changes the power_mode of the sensor of a certain channel

        #power supply operation mode may be important during measurements, as the light of the sensor will influence
        the measurements, disable the sensor when you are taking a measurement, power_save is somewhere in the middle
        with less sensor light(also less heat produced) but presumably either less accuracy or slower adjustments,
        can be usefull for allignment with smaract stages

        moving to an absolute position requires the power_mode to be enabled


        :param mode: which operation mode
                    0: disabled
                        1: enabled
                        2: powersave

        """
        # for i in range(self.numofchan):
        #     channel_idx=c_uint(i)
        self.dll.SA_SetSensorEnabled_S(self.MCS_HANDLE,c_uint(mode))
        self.power_mode=mode

    def get_power_mode(self):
        """
        asks the current powermode and stores it in self.powermode
        :return:
        """
        getmode=c_uint()
        self.dll.SA_GetSensorEnabled_S(self.MCS_HANDLE,byref(getmode))

        self.powermode=getmode.value
        return self.powermode


class MCS2(MCS2_Bare, MotionControllerMultiAxis):
    """ Driver for SCU controller with multiple axis

    """
    def __init__(self, device_locator=None, dll='MCSControl', *args, **kwargs):
        """ Set default settings for device

        :param device_locator: string, eg:
                'usb:sn:<serial>'
                'usb:ix:<n>'
                'network:sn:<serial>'
                'network:<ip>'
        :param dll: name of dll or so object. Should be found by ld
        """
        super().__init__(*args, **kwargs)
        self.stage = SmaractStage

    def initialize(self):
        super().initialize()
        self.detect_axis()

    def query(self, command, *, send_args=(None, None), recv_args=(None, None)):
        return MotionControllerMultiAxis.query(self, ':{}'.format(command),
                                 send_args=send_args, recv_args=recv_args)

    def write(self, command, *args, **kwargs):
        return MotionControllerMultiAxis.write(self,':{}'.format(command),
                                 *args, **kwargs)

    @Feat()
    def idn(self):
        return self.parse_query('I', format='I{:s}')

    @Action()
    def detect_axis(self):
        """ Find the number of axis available.

        The detection stops as soon as an empty controller is found.
        """
        pass

#TODO:
class MotionAxis(MotionAxisMultiple, BacklashMixing):
    def __del__(self):
        self.parent = None
        self.num = None

    def query(self, command, *, send_args=(None, None), recv_args=(None, None)):
        return self.parent.query('{:d}{}'.format(self.num, command),
                                 send_args=send_args, recv_args=recv_args)

    def write(self, command, *args, **kwargs):
        return self.parent.write('{:d}{}'.format(self.num, command),
                                 *args, **kwargs)

    @Feat()
    def idn(self):
        return self.query('ID?')

    @Action()
    def on(self):
        """Put axis on"""
        self.write('MO')

    @Action()
    def off(self):
        """Put axis on"""
        self.write('MF')

    @Feat(values={True: '1', False: '0'})
    def is_on(self):
        """
        :return: True is axis on, else false
        """
        return self.query('MO?')

    @Action(units='mm')
    def define_home(self, val=0):
        """Remap current position to home (0), or to new position

        :param val: new position"""
        self.write('DH%f' % val)

    @Action()
    def home(self):
        """Execute the HOME command"""
        self.write('OR')

    @Feat(units='mm')
    def position(self):
        return self.query('TP?')

    @position.setter
    def position(self, pos):
        """
        Waits until movement is done if self.wait_until_done = True.

        :param pos: new position
        """
        if not self.is_on:
            self.log_error('Axis not enabled. Not moving!')
            return

        # First do move to extra position if necessary
        self._set_position(pos, wait=self.wait_until_done)


    def __set_position(self, pos):
        """
        Move stage to a certain position
        :param pos: New position
        """
        self.write('PA%f' % (pos))
        self.last_set_position = pos

    @Feat(units='mm/s')
    def max_velocity(self):
        return float(self.query('VU?'))

    @max_velocity.setter
    def max_velocity(self, velocity):
        self.write('VU%f' % (velocity))

    @Feat(units='mm/s**2')
    def max_acceleration(self):
        return float(self.query('AU?'))

    @max_acceleration.setter
    def max_acceleration(self, velocity):
        self.write('AU%f' % (velocity))

    @Feat(units='mm/s')
    def velocity(self):
        return float(self.query('VA?'))

    @velocity.setter
    def velocity(self, velocity):
        """
        :param velocity: Set the velocity that the axis should use when moving
        :return:
        """
        self.write('VA%f' % (velocity))

    @Feat(units='mm/s**2')
    def acceleration(self):
        return float(self.query('VA?'))

    @acceleration.setter
    def acceleration(self, acceleration):
        """
        :param acceleration: Set the acceleration that the axis should use
                             when starting
        :return:
        """
        self.write('AC%f' % (acceleration))

    @Feat(units='mm/s')
    def actual_velocity(self):
        return float(self.query('TV'))

    @actual_velocity.setter
    def actual_velocity(self, val):
        raise NotImplementedError

    @Action()
    def stop(self):
        """Emergency stop"""
        self.write('ST')

    @Feat(values={True: '1', False: '0'})
    def motion_done(self):
        return self.query('MD?')

    # Not working yet, see https://github.com/hgrecco/lantz/issues/35
    # @Feat(values={Q_('encodercount'): 0,
    #                     Q_('motor step'): 1,
    #                     Q_('millimeter'): 2,
    #                     Q_('micrometer'): 3,
    #                     Q_('inches'): 4,
    #                     Q_('milli-inches'): 5,
    #                     Q_('micro-inches'): 6,
    #                     Q_('degree'): 7,
    #                     Q_('gradian'): 8,
    #                     Q_('radian'): 9,
    #                     Q_('milliradian'): 10,
    #                     Q_('microradian'): 11})
    @Feat()
    def units(self):
        ret = int(self.query(u'SN?'))
        return UNITS[ret]

    @units.setter
    def units(self, val):
        # No check implemented yet
        self.write('%SN%' % (self.num, UNITS.index(val)))
        super().units = val

    def _wait_until_done(self):
        # wait_time = convert_to('seconds', on_dimensionless='warn')(self.wait_time)
        time.sleep(self.wait_time)
        while not self.motion_done:
            time.sleep(self.wait_time)
        return True
