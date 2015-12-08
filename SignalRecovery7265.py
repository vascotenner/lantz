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
    TERMINATOR = [EOI]
    TECH ECHO = DISABLED

    SDC=ADF 1 ENABLED
    """

    DEFAULTS = {'COMMON': {'write_termination': '',
                           'read_termination': ''}}

    sensitivities = {}

    time_constants = {0: 10e-6, 1: 20e-6, 2: 40e-6, 3: 80e-6, 4: 160e-6,
                      5: 320e-6, 6: 640e-6, 7: 5e-3, 8: 10e-3, 9: 20e-3,
                      10: 50e-3, 11: 100e-3, 12: 0.2, 13: 0.5, 14: 1, 15: 2,
                      16: 5, 17: 10, 18: 20, 19: 50, 20: 100, 21: 200, 22: 500,
                      23: 1e3, 24: 2e3, 25: 5e3, 26: 10e3, 27: 20e3, 28: 50e3,
                      29: 100}

    # time_constants = {10e-6: 0, 20e-6: 1, 40e-6: 2, 80e-6: 3,
    #                    160e-6: 4, 320e-6: 5, 640e-6: 6, 5e-3: 7,
    #                    10e-3: 8, 20e-3: 9, 50e-3: 10, 100e-3: 11,
    #                    200e-3: 12, 500e-3: 13, 1: 14, 2: 15, 5: 16,
    #                    10: 17, 20: 18, 50: 19, 100: 20, 200: 21,
    #                    500: 22, 1e3: 23, 2e3: 24, 5e3: 25, 10e3: 26,
    #                    20e3: 27, 50e3: 28, 100: 29}

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
        read = self.query('X.')
        return float(read.replace('\x00', ''))

    @Feat()
    def y(self):
        """
        Read y value from lockin.
        """
        read = self.query('Y.')
        return float(read.replace('\x00', ''))

    @Feat()
    def xy(self):
        """
        Read x and y values from lockin simultaneously.
        """
        read = self.query('XY.')
        return [float(x) for x in read.replace('\x00', '').split(',')]

    @Feat()
    def magnitude(self):
        """
        Read signal magnitude from lockin.
        """
        read = self.query('MAG.')
        return float(read.replace('\x00', ''))

    @Feat()
    def phase(self):
        """
        Read signal phase from lockin.
        """
        read = self.query('PHA.')
        return float(read.replace('\x00', ''))

    @Feat()
    def mag_phase(self):
        """
        Read signal magnitude and phase from lockin.
        """
        read = self.query('MP.')
        return [float(x) for x in read.replace('\x00', '').split(',')]

    # TODO: time constant
    @Feat(limits=(0, 29, 1))
    def time_constant_integer(self):
        """
        Read current lockin time constant mode setting
        """
        return int(self.query('TC'))

    @time_constant_integer.setter
    def time_constant_integer(self, integer):
        """
        Set lockin time constant.
        """
        return self.write('TC{}'.format(integer))

    @Feat(values=time_constants)
    def time_constant(self):
        """
        Returns current time constant setting (in seconds).
        """
        return float(self.query('TC.'))

    @time_constant.setter
    def time_constant(self, time_const):
        """
        Sets the current time constant setting (in seconds).
        """
        return self.write('TC.{}'.format(time_const))

    @Feat()
    def frequency(self):
        """
        Read current signal frequency.
        """
        read = self.query('FRQ.')
        return float(read.replace('\x00', ''))

    @Feat(limits=(0, 250e3))
    def oscillator_freq(self):
        """
        Read internal oscillator frequency.
        """
        return float(self.query('OF.'))

    @oscillator_freq.setter
    def oscillator_freq(self, frequency):
        """
        Set internal oscillator frequency.
        """
        return self.write('OF.{}'.format(frequency))

    # TODO: gain

    # TODO: sensitivity

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
        return self.write('IE {}'.format(value))


if __name__ == '__main__':
    with SignalRecovery7265('GPIB0::7::INSTR') as inst:
        print('The instrument identification is ' + inst.idn)

        print('Testing signal readings')
        print('Signal X component is ' + str(inst.x) + 'V')
        print('Signal Y component is ' + str(inst.y) + 'V')
        print('Signal magnitude is ' + str(inst.magnitude) + 'V')
        print('Signal phase is ' + str(inst.phase) + 'degrees')

        print('Testing full quadrature readings')
        print('XY measurement: ' + str(inst.xy))
        print('magnitude and phase measurement: ' + str(inst.mag_phase))

        print('What\'s the frequency, Kenneth?')
        print('Reference frequency: ' + str(inst.frequency) + 'Hz')
        inst.oscillator_freq = 137.0
        print('Reference frequency: ' + str(inst.frequency) + 'Hz')
        inst.oscillator_freq = 17
        print('Reference frequency: ' + str(inst.frequency) + 'Hz')
        #
        print('Internal External Reference check')
        print('Internal/ext reference: ' + inst.int_ext_ref)
        inst.int_ext_ref = 'ext'
        print('Internal/ext reference: ' + inst.int_ext_ref)
        inst.int_ext_ref = 'int'
        print('Internal/ext reference: ' + inst.int_ext_ref)

        print('Time constant check')
        print('Int TC: ' + str(inst.time_constant_integer))
        print('TC (sec): ' + str(inst.time_constant))
        inst.time_constant_integer = 15
        print('Int TC: ' + str(inst.time_constant_integer))
        print('TC (sec): ' + str(inst.time_constant))
        inst.time_constant = 100e-3
        print('Int TC: ' + str(inst.time_constant_integer))
        print('TC (sec): ' + str(inst.time_constant))
