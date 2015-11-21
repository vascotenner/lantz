# Lakeshore 332 Temperature Controller Driver
# Peter Mintun <pmintun@uchicago.edu>

# This file is a driver for the Lakeshore 332 series temperature controller.

# Some sort of license information goes here.

from lantz import Feat, Action
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
                          'read_termination': '\n'}}

    channel_list = ['A','B']
    heater_range_vals = {'off': 0, 'low': 1, 'medium': 2, 'high': 3}
    heater_status_vals = {'no error':0, 'open load':1, 'short':2}
    controller_modes = {'local': 0, 'remote':1, 'remote, local lockout': 2}

    # def __init__(self, GPIB_name, GPIB_addr, reset=False):
    #    res_name = GPIB_name + '::' + GPIB_addr + '::INSTR'
    #    super().__init__(res_name, name='Lakeshore332')
    #    self._address = res_name
    _verbose = True
    #    self._idn = None
    #
    #    print(res_name)
    #
    #    print(self.channel_list)
    #    print(self.heater_range_vals)
    #    print(self.heater_status_vals)
    #    print(self.controller_modes)



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

    @Action()
    def reset(self):
         """
         Resets the Lakeshore 332 temperature controller.
         """
         self.write('*RST')

    @Feat()
    def idn(self):
        """
        Returns the instrument identification.
        """
        return self.query('*IDN?')

    @Feat()
    def kelvin(self, channel):
         """
         Returns temperature reading from specified channel in Kelvin.
         """
         if channel in channel_list:
             return self.query('KRDG?{}'.format(channel))
         else:
             print('Error: invalid channel')
             return None

    @Feat()
    def get_sensor(self, channel):
        """
        Returns sensor reading from specified channel.
        """
        if channel in channel_list:
            msg_str = 'SRDG?' + channel
            return self.query(msg_str.format(channel))
        else:
            print('Error: invalid channel')
            return None

    #@Feat(values = self.heater_status_vals)
    @Feat()
    def get_heater_status(self):
        """
        Returns the heater status.
        """
        ans = self.query('HTRST?')
        if self._verbose:
            if ans == '0':
                print('Heater status: no error')
            elif ans == '1':
                print('Heater status: open load')
            elif ans == '2':
                print('Heater status: short')
            else:
                print('Error: Heater status invalid')
        return ans

    #@Feat(values=self.heater_range_vals)
    @Feat()
    def heater_range(self):
        """
        Queries the instrument, prints a message describing the current heater
        range setting, then returns the heater range value.
        """
        ans = self.query('RANGE?')
        if self._verbose:
            if ans == '0':
                print('Heater range: off')
            elif ans == '1':
                print('Heater range: low')
            elif ans == '2':
                print('Heater range: medium')
            elif ans == '3':
                print('Heater range: high')
            else:
                print('Error: Heater not responding correctly')
        return ans

    @heater_range.setter
    def heater_range(self, heater_setting):
        """
        Sets heater range to  heater_setting.

        heater_setting must be an integer between 0 and 3 inclusive.
        """
        return self.write('RANGE {}'.format(heater_setting))


    #@Feat(values=self.controller_modes)
    @Feat()
    def mode(self):
        """
        Reads the mode setting of the controller.
        """
        return self.query('MODE?')

    @mode.setter
    def mode(self, mode):
        """
        Sets controller mode, valid mode inputs are:
        local
        remote
        remote, local lockout
        """
        return self.query('MODE {}'.format(value))

    def local(self):
        self.set_mode('local')

    def remote(self):
        self.set_mode('remote')

    @Feat()
    def pid(self, channel):
        ans = self.query('PID? {}'.format(channel))
        fields = ans.split(',')
        if len(fields) != 3:
            return None
        fields = [float(f) for f in fields]
        return fields

    @pid.setter
    def pid(self, val, channel):
        """
        Need to actually implement this!
        """
        print('This feature is actually unimplemented! Sorry!')

    @Feat()
    def setpoint(self, channel):
        """
        Return the feedback controller's setpoint.
        """
        if channel in self.channel_list:
            return self.query('SETP?{}'.format(channel))
        else:
            return None

    @setpoint.setter
    def setpoint(self, channel, value):
        """
        Sets the setpoint of channel channel to value value
        """
        #TODO: actually implement this!
        print('Not yet implemented!')

    @Feat()
    def mout(self):
        """
        """
        #TODO: actually implement this!
        print('Not yet implemented!')

    @mout.setter
    def mout(self, value):
        """
        """
        #TODO: actually implement this!
        print('Not yet implemented!')

    @Feat()
    def cmd_mode(self):
        """
        """
        #TODO: actually implement this!
        print('Not yet implemented!')

    @cmd_mode.setter
    def cmd_mode(self, value):
        """
        """
        #TODO: implement this!
        print('Not yet implemented!')






if __name__ == '__main__':
    with Lakeshore332('GPIB0::16::INSTR') as inst:
        print('The instrument identification is ' + inst.idn)
        #print('The current temperature is '+ inst.kelvin(channel='A'))
        #inst.initialize(reset=False)
