from lantz import Feat, DictFeat, Action
from lantz.messagebased import MessageBasedDriver

from time import sleep


class SignalRecovery7265(MessageBasedDriver):
    """Signal Recovery 7265
    DSP Lock-in Amplifier

    Author: P. Mintun
    Version: 0.0.1
    Date: 11/13/2015

    "Stay safe and happy locking in..."

    This driver assumes that the COMM settings of the 7265 are set up as
    follows:

    ADDRESS = N
    TERMINATOR = [CR],[LF]
    TECH ECHO = DISABLED

    SDC=ADF 1 ENABLED
    """

    DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}

    sensitivities = {}

    time_constants = {0: '10e-6', 1: '20e-6', 2: '40e-6', 3: '80e-6',
                      4: '160e-6', 5: '320e-6', 6: '640e-6', 7: '5e-3',
                      8: '10e-3', 9: '20e-3', 10: '50e-3', 11: '100e-3',
                      12: '200e-3', 13: '500e-3', 14: '1', 15: '2', 16: '5',
                      17: '10', 18: '20', 19: '50', 20: '100', 21: '200',
                      22: '500', 23: '1e3', 24: '2e3', 25: '5e3', 26: '10e3',
                      27: '20e3', 28: '50e3', 29: '100'}

    int_ext_refs = {'int': 0, 'rear ext': 1, 'ext': 2}

    @Feat()
    def idn(self):
        """
        Returns current instrument identification.
        """
        return self.query('ID')

    @Feat()
    def x(self):
        """
        Read x value from lockin.
        """
        return float(self.query('X.'))

    @Feat()
    def y(self):
        """
        Read y value from lockin.
        """
        return float(self.query('Y.'))

    @Feat()
    def xy(self):
        """
        Read x and y values from lockin simultaneously.
        """
        return self.query('XY.')

    @Feat()
    def magnitude(self):
        """
        Read signal magnitude from lockin.
        """
        return float(self.query('MAG.'))

    @Feat()
    def phase(self):
        """
        Read signal phase from lockin.
        """
        return float(self.query('PHA.'))

    @Feat()
    def mag_phase(self):
        """
        Read signal magnitude and phase from lockin.
        """
        return self.query('MP.')

    # TODO: time constant
    @Feat()
    def time_constant(self):
        """
        Read current lockin time constant
        """
        print('not implemented yet')
        return 0

    @time_constant.setter
    def time_constant(self, value):
        """
        Set lockin time constant.
        """
        print('not implemented yet')
        return 0

    # TODO: frequency
    @Feat()
    def frequency(self):
        """
        Read current signal frequency.
        """
        return float(self.query('FRQ.'))

    @frequency.setter
    def frequency(self, freq):
        """
        Returns the frequency of the reference signal (either internal or
        externally sourced) in Hz.
        """
        print('not implemented yet')
        return 0

    # TODO: gain

    # TODO: sensitivity

    # TODO: reference internal/external
    @Feat(values=int_ext_refs)
    def int_ext_ref(self):
        """
        Check if lockin is internally or externally referenced
        """
        return int(self.query('IE'))

    @int_ext_ref.setter
    def int_ext_ref(self, value):
        """
        Set lockin to be internal or external reference
        """
        # TODO: fix this!
        print('Warning: fails intermittently, need to fix')
        return self.query('IE {}'.format(value))


if __name__ == '__main__':
    with SignalRecovery7265('GPIB0::7::INSTR') as inst:
        print('The instrument identification is ' + inst.idn)

        print('Testing signal readings')
        print('Signal X component is ' + str(inst.x) + 'V')
        print('Signal Y component is ' + str(inst.y) + 'V')
        print('Signal magnitude is ' + str(inst.magnitude) + 'V')
        print('Signal phase is ' + str(inst.phase) + 'degrees')

        print('Testing full quadrature readings')
        print('XY measurement: ' + inst.xy)
        print('magnitude and phase measurement: ' + inst.mag_phase)

        print('Internal External Reference check')
        print('Internal/ext reference: ' + inst.int_ext_ref)
        #inst.int_ext_ref = 'ext'
        print('Internal/ext reference: ' + inst.int_ext_ref)
        #inst.int_ext_ref = 'int'
        print('Internal/ext reference: ' + inst.int_ext_ref)
