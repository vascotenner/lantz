# Lakeshore 332 Temperature Controller Driver
# Peter Mintun <pmintun@uchicago.edu>

# This file is a driver for the Lakeshore 332 series temperature controller.

# Some sort of license information goes here.

from lantz import Feat, Action
from lantz.messagebased import MessageBasedDriver

class Lakeshore332(MessageBasedDriver):
    """
    Lakeshore 332 Temperature controlller.

    This class implements a set of basic controls for the Lakeshore 332 series
    temperature controller.

    Full documentation of the device is available at:
    http://www.lakeshore.com/ObsoleteAndResearchDocs/332_Manual.pdf
    """

    def __init__(self, name, address, reset=False):
        MessageBasedDriver.__init__(self,name)
        self._address = address
        self._verbose = True

        self.channel_list = ['A','B']
        self.heater_range_vals = {'off': 0, 'low': 1, 'medium': 2, 'high': 3}
        self.heater_status_vals = {'no error':0, 'open load':1, 'short':2}
        self.controller_modes = {'local': 0, 'remote':1, 'remote, local lockout': 2}

        if reset:
            self.reset()
        else:
            self.get_all()

     DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}


    @Action()
    def reset(self):
        """
        Resets the Lakeshore 332 temperature controller.
        """
        self.write('*RST')

    def get_all(self):
        """
        Gets the instrument identification and mode.
        """
        print(self.idn())
        print(self.mode())
        return None

    @Feat()
    def get_idn(self):
        """
        Returns the instrument identification.
        """
        return self.query('*IDN?')

    @Feat()
    def get_kelvin(self, channel):
        """
        Returns temperature reading from specified channel in Kelvin.
        """
        if channel in channel_list:
            msg_str = 'KRDG?' + channel
            return self.query(msg_str.format(channel))
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

    @Feat(values=self.heater_status_vals)
    def get_heater_status(self):
        """
        Returns the header status.
        """
        ans = self.query('HTRST?')
        if self._verbose:
            if ans == '0':
                print('Heater status: no error)
            elif ans == '1':
                print('Heater status: open load')
            elif ans == '2':
                print('Heater status: short')
            else:
                print('Error: Heater status invalid')
        return ans

    @Feat(values=self.heater_range_vals)
    def get_heater_range(self):
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


    @Feat(values=controller_modes)
    def get_mode(self):
        """
        Reads the mode setting of the controller.
        """
        return self.query('MODE?')

    @get_mode.setter
    def get_mode(self, mode):
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

    @get_pid.setter
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
    with Lakeshore332('GPIB::GPIB0::16::INSTR') as inst:
        print('The identification of this instrument is : ' + inst.idn)
