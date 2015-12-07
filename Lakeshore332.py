# Lakeshore 332 Temperature Controller Driver
# Peter Mintun <pmintun@uchicago.edu>

# This file is a driver for the Lakeshore 332 series temperature controller.

# Some sort of license information goes here.

from lantz import Feat, Action, DictFeat
from lantz.messagebased import MessageBasedDriver

class Lakeshore332(MessageBasedDriver):
    """
    Lakeshore 332 Temperature controlller.

    This class, based off of the Lantz MessageBasedDriver class, implements a
    set of basic controls for the Lakeshore 332 series temperature controller.
    It essentially a port of a nice driver written for QtLab by Reinier Heeres.

    Full documentation of the device is available at:
    http://www.lakeshore.com/ObsoleteAndResearchDocs/332_Manual.pdf
    """

    # These defaults assume that you have set the IEEE Term setting to: Lf Cr
    DEFAULTS = {'COMMON': {'write_termination': '\n',
                          'read_termination': ''}}

    GPIB_name = None
    GPIB_address = -1

    channels = ['a', 'b']
    heater_range_vals = {'off': 0, 'low': 1, 'medium': 2, 'high': 3}
    heater_status_vals = {'no error':0, 'open load':1, 'short':2}
    controller_modes = {'local': 0, 'remote': 1, 'remote, local lockout': 2}

    T_min = 0
    T_max = 350

    T_min_set = 1.8
    T_max_set = 350

    # def __init__(self, GPIB_name, GPIB_addr, reset=False):
    #    res_name = GPIB_name + '::' + GPIB_addr + '::INSTR'
    #    super().__init__(res_name, name='Lakeshore332')
    #    self._address = res_name
    _verbose = True

    # def query(self, command, *, send_args=(None, None), recv_args=(None, None)):
    #      answer = super().query(command, send_args=send_args, recv_args=recv_args)
    #      if answer == 'ERROR':
    #          raise InstrumentError
    #          return answer

    #def initialize(self, reset=False):
    #    """
    #    Initialization code for Lakeshore 332 should go in this function, since
    #    if you define functions as @Feats() they cannot be executed in the
    #    __init__ function.
    #    """
        #if (self._verbose):
            #print('initializing Lakeshore 332...')

        #if reset:
            #if self._verbose:
                #print('Resetting...')
            #self.reset
        #else:
            #self.idn()
            #self.mode()

    # def get_all(self):
    #    """
    #    Gets the instrument identification and mode.
    #    """
    #    self.idn()
    #    self.mode()
    @Feat()
    def idn(self):
        """
        Returns the instrument identification.
        """
        print('getting IDN')
        return self.query('*IDN?')

    @Action()
    def reset(self):
         """
         Resets the Lakeshore 332 temperature controller.
         """
         print("resetting")
         self.write('*RST')
         print("reset")

    @DictFeat(limits=(T_min,T_max), keys=channels)
    def kelvin_meas(self, channel):
          """
          Returns measured temperature reading from specified channel in Kelvin.
          """
          return float(self.query('KRDG?{}'.format(channel)))

    @DictFeat(keys=channels)
    def sensor(self, channel):
        """
        Returns sensor reading from specified channel.
        """
        return float(self.query('SRDG?{}'.format(channel)))

    @Feat(values=heater_status_vals)
    def heater_status(self):
        """
        Returns the heater status.
        """
        return int(self.query('HTRST?'))

    @Feat(values=heater_range_vals)
    def heater_range(self):
        """
        Queries the instrument, prints a message describing the current heater
        range setting, then returns the heater range value.
        """
        return int(self.query('RANGE?'))

    @heater_range.setter
    def heater_range(self, heater_setting):
        """
        Sets heater range to  heater_setting.

        heater_setting must be an integer between 0 and 3 inclusive.
        """
        return self.write('RANGE {}'.format(heater_setting))


    @Feat(values=controller_modes)
    def mode(self):
        """
        Reads the mode setting of the controller.
        """
        return int(self.query('MODE?'))

    @mode.setter
    def mode(self, mode):
        """
        Sets controller mode, valid mode inputs are:
        local (0)
        remote (1)
        remote, local lockout (2)
        """
        return self.query('MODE{}'.format(mode))

    @Feat()
    def pid(self, channel):
        """
        Get parameters for PID loop.
        """
        print('PID loop not yet implemented')
        return 0
    #     ans = self.query('PID? {}'.format(channel))
    #     fields = ans.split(',')
    #     if len(fields) != 3:
    #         return None
    #     fields = [float(f) for f in fields]
    #     return fields
    #
    @pid.setter
    def pid(self, val, channel):
         """
         Get parameters for PID loop
         """
         print('This feature is actually unimplemented! Sorry!')
         return 0

    @DictFeat(limits=(T_min_set,T_max_set), keys=channels)
    def setpoint(self, channel):
          """
          Return the temperature controller setpoint.
          """
          return float(self.query('SETP?{}'.format(channel)))

    @setpoint.setter
    def setpoint(self, channel, T_set):
         """
         Sets the setpoint of channel channel to value value
         """
         print('Error: not implemented correctly')
         return self.query('SETP{} {}'.format(channel,T_set))
    #
    # @Feat()
    # def mout(self):
    #     """
    #     """
    #     #TODO: actually implement this!
    #     print('Not yet implemented!')
    #
    # @mout.setter
    # def mout(self, value):
    #     """
    #     """
    #     #TODO: actually implement this!
    #     print('Not yet implemented!')
    #


if __name__ == '__main__':
    with Lakeshore332('GPIB0::16::INSTR') as inst:
        print('Getting instrument identification...')
        #inst.query('*IDN?')
        print('The instrument identification is ' + inst.idn)

        print('resetting...')
        inst.reset
        print('reset.')

        # Testing mode switching functionality
        print('The current mode is ' + inst.mode + '.')
        inst.mode = 'remote, local lockout'
        print('Now the mode is ' + inst.mode + '.')
        inst.mode = 'remote'
        print('Now the mode is ' + inst.mode + '.')

        # Testing Kelvin read functionality
        print('Current temperature on channel a is ' + str(inst.kelvin_meas['a'])
        + ' Kelvin')
        print('Current temperature on channel b is ' + str(inst.kelvin_meas['b'])
        + ' Kelvin')

        # Testing sensor reading functionality
        print('Sensor reading on channel a is ' + str(inst.sensor['a']))
        print('Sensor reading on channel b is ' + str(inst.sensor['b']))

        # Testing heater status
        print('Heater status is ' + str(inst.heater_status))

        # Testing heater range
        print('Heater range is ' + str(inst.heater_range))
        inst.heater_range = 'low'
        print('Heater range is ' + str(inst.heater_range))
        inst.heater_range = 'off'
        print('Heater range is ' + str(inst.heater_range))

        # Testing setpoint
        print('Controller a setpoint is ' + str(inst.setpoint['a']))
        inst.setpoint['a'] = 50
        print('Controller a channel setpoint is ' + str(inst.setpoint['a']))
        inst.setpoint['a'] = 300
        print('Controller a channel setpoint is ' + str(inst.setpoint['a']))

        print('Controller b setpoint is ' + str(inst.setpoint['b']))
