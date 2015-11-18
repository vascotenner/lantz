# Lakeshore 332 Temperature Controller Driver
# Peter Mintun <pmintun@uchicago.edu>

# This file is a driver for the Lakeshore 332 series temperature controller.

# Some sort of license information goes here.

from lantz import Feat
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




     DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}







    @Feat()
    def idn(self):
        """
        Returns the instrument identification
        """
        return self.query('*IDN?')

    @Feat()
    def get_kelvin(self, channel):
        """
        Returns Kelvin reading from specified channel
        """
        return self.query('KRDG? {}'.format(channel))

    @Feat()
    def heater_range(self):
        """
        Queries the instrument and prints the current heater range setting.
        """
        ans = self.query('RANGE?')
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

    @heater_range.setter
    def heater_range(self, heater_setting):
        """

        """





if __name__ == '__main__':
    with Lakeshore332('GPIB0::GPIB::16') as inst:
        print('The identification of this instrument is : ' + inst.idn)
