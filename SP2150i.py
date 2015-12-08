from lantz import Feat, DictFeat, Action
from lantz.messagebased import MessageBasedDriver


class SP2150i(MessageBasedDriver):


    max_speed = 100
    wavelength_min = 380
    wavelength_max = 520

    @Feat(limits=(0,max_speed))
    def scan_speed(self):
        """
        Get scan rate in nm/min.
        """
        return float(self.query('?NM/MIN'))

    @scan_speed.setter
    def scan_speed(self, speed):
        """
        Sets current scan speed in nm/min.
        """
        return self.query('{} NM/MIN'.format(speed))

    @Feat(limits=(wavelength_min, wavelength_max))
    def nm(self):
        """
        Returns  wavelength to nm.
        """
        return float(self.query('?NM'))

    @nm.setter
    def nm(self, wavelength):
        """
        Sets output to specified wavelength, traveling at the current scan rate.
        """
        return self.query('{} NM'.format(wavelength))

    @Feat(limits=(1,2,1))
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

    @Feat(limits=(1,3,1))
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
        with SP2150i('USB derp derp derp') as inst:
            print('The instrument identification is ' + inst.idn)
