from lantz import Feat, DictFeat, Action
from lantz.messagebased import MessageBasedDriver

from collections import OrderedDict

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

    INT_EXT_REF = OrderedDict([
                   ('int', 0),
                   ('rear ext', 1),
                   ('ext', 2)
                   ])

    TIME_CONSTANTS = OrderedDict([
                     (0, 10e-6),
                     (1, 20e-6),
                     (2, 40e-6),
                     (3, 80e-6),
                     (4, 160e-6),
                     (5, 320e-6),
                     (6, 640e-6),
                     (7, 5e-3),
                     (8, 10e-3),
                     (9, 20e-3),
                     (10, 50e-3),
                     (11, 100e-3),
                     (12, 0.2),
                     (13, 0.5),
                     (14, 1),
                     (15, 2),
                     (16, 5),
                     (17, 10),
                     (18, 20),
                     (19, 50),
                     (20, 100),
                     (21, 200),
                     (22, 500),
                     (23, 1e3),
                     (24, 2e3),
                     (25, 5e3),
                     (26, 10e3),
                     (27, 20e3),
                     (28, 50e3),
                     (29, 100)
                     ])

    AC_GAINS = OrderedDict([
               ('0dB', 0),
               ('10dB', 1),
               ('20dB', 2),
               ('30dB', 3),
               ('40dB', 4),
               ('50dB', 5),
               ('60dB', 6),
               ('70dB', 7),
               ('80dB', 8),
               ('90dB', 9),
               ])

    SENSITIVITIES = OrderedDict([
                    ('2e-9V', 1),
                    ('5e-9V', 2),
                    ('1e-8V', 3),
                    ('2e-8V', 4),
                    ('5e-8V', 5),
                    ('1e-7V', 6),
                    ('2e-7V', 7),
                    ('5e-7V', 8),
                    ('1e-6V', 9),
                    ('2e-6V', 10),
                    ('5e-6V', 11),
                    ('1e-5V', 12),
                    ('2e-5V', 13),
                    ('5e-5V', 14),
                    ('1e-4V', 15),
                    ('2e-4V', 16),
                    ('5e-4V', 17),
                    ('1e-3V', 18),
                    ('2e-3V', 19),
                    ('5e-3V', 20),
                    ('1e-2V', 21),
                    ('2e-2V', 22),
                    ('5e-2V', 23),
                    ('1e-1V', 24),
                    ('2e-1V', 25),
                    ('5e-1V', 26),
                    ('1V', 27),
                    ])

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

    @Action()
    def autophase(self):
        """
        Adds an offset to the phase of the lockin to minimize the y-channel
        signal and maximize the x-channel signal.
        """
        return self.write('AQN')

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

    @Feat(values=TIME_CONSTANTS)
    def time_constant(self):
        """
        Returns current time constant setting (in seconds).
        """
        return float(self.query('TC.'))

    @time_constant.setter
    def time_constant(self, time_const):
        """
        Not implemented, not a built in functionality.
        """
        print('Error: invalid operation, cannot directly set TC')
        return 0

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

    @Feat(values=AC_GAINS)
    def gain(self):
        """
        Read current AC gain (dB).
        """
        return int(self.query('ACGAIN'))

    @gain.setter
    def gain(self, gain_value):
        """
        Set current AC gain (dB)
        """
        return self.write('ACGAIN{}'.format(gain_value))

    @Feat(values=SENSITIVITIES)
    def sensitivity(self):
        """
        Gets sensitivity according to the SENSITIVITIES table.
        """
        return int(self.query('SEN'))

    # @Feat(values=SENSITIVITIES)
    # def sensitivity_int(self):
    #     """
    #     Returns integer value of sensitivity as described by SENSITIVITIES.
    #     """
    #     return int(self.query('SEN'))

    @sensitivity.setter
    def sensitivity(self, sen_it):
        """
        Sets value of sensitivity as described by SENSITIVITIES.
        """
        return self.write('SEN{}'.format(sen_it))

    @Action()
    def autosensitivity(self):
        """
        Runs an autosensitivity operation.

        The instrument adjusts its full-scale sensitivity so that the magnitude
        output lies between 30-90 percent of full-scale
        """
        a = self.write('AS')
        sleep(7.5)  # wait for operation to complete
        return a

    @Action()
    def autogain(self):
        """
        Set current AC gain to automatic.
        """
        return self.write('AUTOMATIC1')

    @Feat(values=INT_EXT_REF)
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
    with SignalRecovery7265.via_gpib(7) as inst:
        print('The instrument identification is ' + inst.idn)

        print('Testing signal readings')
        print('Signal X: {}V'.format(inst.x))
        print('Signal Y: {}V'.format(inst.y))
        print('Signal magnitude: {}V'.format(inst.magnitude))
        print('Signal phase: {}degrees'.format(inst.phase))

        print('Testing full quadrature readings')
        print('X,Y: {}V'.format(list(inst.xy)))
        print('Magnitude, Phase: {}'.format(list(inst.mag_phase)))
        inst.autophase
        sleep(2)
        print('Magnitude, Phase: {}'.format(list(inst.mag_phase)))

        print('Testing frequency code')
        print('Ref f: {}Hz'.format(inst.frequency))
        inst.oscillator_freq = 137.0
        print('Ref f: {}Hz'.format(inst.frequency))
        inst.oscillator_freq = 17
        print('Ref f: {}Hz'.format(inst.frequency))
        #
        print('Internal External Reference check')
        print('Internal/ext reference: {}'.format(inst.int_ext_ref))
        inst.int_ext_ref = 'ext'
        print('Internal/ext reference: {}'.format(inst.int_ext_ref))
        inst.int_ext_ref = 'int'
        print('Internal/ext reference: {}'.format(inst.int_ext_ref))

        print('Time constant check')
        print('Int TC: {}'.format(inst.time_constant_integer))
        print('TC (sec): {}s'.format(inst.time_constant))
        inst.time_constant_integer = 15
        print('Int TC: {}'.format(inst.time_constant_integer))
        print('TC (sec): {}s'.format(inst.time_constant))
        inst.time_constant_integer = 10
        print('Int TC: {}'.format(inst.time_constant_integer))
        print('TC (sec): {}s'.format(inst.time_constant))

        print('AC Gain Check')
        print('AC Gain: {}'.format(inst.gain))
        inst.gain = '30dB'
        print('AC Gain: {}'.format(inst.gain))
        inst.autogain
        print('AC Gain: {}'.format(inst.gain))

        print('Sensitivity Check')
        print('Sen: {}'.format(inst.sensitivity))
        inst.sensitivity = '2e-8V'
        print('Sen: {}'.format(inst.sensitivity))
        inst.autosensitivity()
        print('Sen: {}'.format(inst.sensitivity))
