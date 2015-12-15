from lantz import Feat, DictFeat, Action
from lantz.messagebased import MessageBasedDriver

from time import sleep


class SP2150i(MessageBasedDriver):
    """

    """
    MANUFACTURER_ID = '0x0647'
    MODEL_CODE = '0x0100'

    DEFAULTS = {'COMMON': {'write_termination': '\r',
                           'read_termination': ''}}

    max_speed = 100
    wavelength_min = 380
    wavelength_max = 520

    def clear_buffer(self):
        """
        Clears buffer to avoid issues w/ commands being stuck in buffer.
        """
        return 0

    @Feat(limits=(0, max_speed))
    def scan_speed(self):
        """
        Get scan rate in nm/min.
        """
        return self.query('?NM/MIN')

    @scan_speed.setter
    def scan_speed(self, speed):
        """
        Sets current scan speed in nm/min.
        """
        self.clear_buffer()
        read = self.query('{} NM/MIN'.format(speed))
        read2 = read.replace('nm/min  ok', '')
        print('nm/min read:' + read2)
        sleep(1)
        return read

    @Feat(limits=(wavelength_min, wavelength_max))
    def nm(self):
        """
        """
        print('Sending ?NM...')
        read = self.query('?NM')
        read = read.replace('nm  ok', '')
        read = read.replace('1` ', '')
        return float(read)

    @nm.setter
    def nm(self, wavelength):
        """
        Sets output to specified wavelength, traveling at the current scan
        rate.
        """
        return self.query('{} NM'.format(wavelength))

    @Feat(limits=(1, 2, 1))
    def grating(self):
        """
        Returns the current grating position
        """
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
        return self.query('{} TURRET'.format(turr_set))

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
    with SP2150i('USB0::0x0647::0x0100::NI-VISA-120001::RAW') as inst:
        print('Testing 1, 2, 3')
        print('Wavelength: {}'.format(inst.nm))
        print('Scan rate: {}'.format(inst.scan_speed))
        # inst.nm = 400.0
