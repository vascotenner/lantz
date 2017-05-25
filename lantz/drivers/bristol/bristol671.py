from lantz.messagebased import MessageBasedDriver
from lantz import Feat, Action

class Bristol671(MessageBasedDriver):

    @Feat()
    def idn(self):
        return self.query('*IDN?')

    @Feat(units='nm')
    def wavelength(self):
        return float(self.query(':MEAS:WAV?'))

    @Feat(units='GHz')
    def frequency(self):
        return float(self.query(':MEAS:FREQ?'))

    @Feat(units='mW')
    def power(self):
        self.write(':UNIT:POW MW')
        return float(self.query(':MEAS:POW?'))
