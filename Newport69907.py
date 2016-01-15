from lantz import Feat, DictFeat, Action
from lantz.messagebased import MessageBasedDriver

from pyvisa import constants

from time import sleep


class SP2150i(MessageBasedDriver):
    """

    """
    DEFAULTS = {'ASRL': {'write_termination': '\r',
                         'read_termination': '',
                         'baud_rate': 9600,
                         'data_bits': 8,
                         'parity': constants.Parity.none,
                         'stop_bits': constants.StopBits.one,
                         'encoding': 'latin-1',
                         'timeout': 10000}}

    max_speed = 100
    wavelength_min = 380
    wavelength_max = 520

    def initialize(self):
        """
        """
        super().initialize()
        self.clear_buffer()

    def clear_buffer(self):
        """
        This function sends an empty query just to clear any junk from the read
        buffer...This could probably be done more elegantly...but it works, for
        now at least.
        """
        result = self.resource.query('')

    @Feat(limits=(wavelength_min, wavelength_max))
    def nm(self):
        """
        Returns current wavelength of monochromater.
        """
        self.clear_buffer()
        read = self.query('?NM')
        wavelength = read.replace('nm  ok', '')
        return float(wavelength)

    @nm.setter
    def nm(self, wavelength):
        """
        Sets output to specified wavelength, traveling at the current scan
        rate.
        """
        self.clear_buffer()
        return self.query('{} NM'.format(wavelength))

    @Feat(limits=(0, max_speed))
    def scan_speed(self):
        """
        Get scan rate in nm/min.
        """
        self.clear_buffer()
        read = self.query('?NM/MIN')
        speed = read.replace('nm/min  ok', '')
        return float(speed)

    @scan_speed.setter
    def scan_speed(self, speed):
        """
        Sets current scan speed in nm/min.
        """
        self.clear_buffer()
        read = self.query('{}NM/MIN'.format(speed))
        speed = read.replace('nm/min  ok', '')
        return float(speed)

    @Feat(limits=(1, 2, 1))
    def grating(self):
        """
        Returns the current grating position
        """
        self.clear_buffer()
        return int(self.query('?GRATING'))

    @grating.setter
    def grating(self, grating_num):
        """
        Sets the current grating to be grating_num
        """
        print('Warning: will wait 20 seconds to change grating.')
        self.query('{} GRATING'.format(grating_num))
        sleep(20)

    @Feat(limits=(1, 3, 1))
    def turret(self):
        """
        Returns the selected turret number.
        """
        return int(self.query('?TURRET'))

    @turret.setter
    def turret(self, turr_set):
        """
        Selects the parameters for the grating on turret turr_set
        """
        return self.query('{}TURRET'.format(turr_set))

    @Feat()
    def turret_spacing(self):
        """
        Returns the groove spacing of the grating for each turret.
        """
        return self.query('?TURRETS')

    @Feat()
    def grating_settings(self):
        """
        Returns the groove spacing and blaze wavelength of grating positions
        1-6. This corresponds to 2 grating positions for each of the 3 turrets
        """
        return self.query('?GRATINGS')


if __name__ == '__main__':
    with SP2150i('ASRL4::INSTR') as inst:
        print('Wavelength: {}nm'.format(inst.nm))
        print('Scan rate: {}nm/min'.format(inst.scan_speed))
            #inst.nm = 400.0
