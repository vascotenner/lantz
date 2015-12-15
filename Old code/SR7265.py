from lantz import Feat, DictFeat, Action
from lantz.messagebased import MessageBasedDriver


class SignalRecovery7265(MessageBasedDriver):
    """Signal Recovery 7265
    DSP Lock-in Amplifier

    Author: P. Mintun
    Version: 0.0.1
    Date: 11/13/2015

    "Stay safe and happy locking in..."

    This driver assumes that the COMM settings of the 7265 are set up as follows:

    ADDRESS = N
    TERMINATOR = [CR],[LF]
    TECH ECHO = DISABLED

    SDC=ADF 1 ENABLED
    """

    DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}



    # Instrument Identification
    @Feat()
    def idn(self):
        """Identification, should output 7265.
        """
        return self.query('ID')

    @Feat()
    def firmware_rev(self):
        print(self.query('REV'))
        return 0
        #return self.query('REV')

    @Feat()
    def firmware_ver(self):
        return self.query('VER')



    def query(self, command, *, send_args=(None, None), recv_args=(None, None)):
        answer = super().query(command, send_args=send_args, recv_args=recv_args)
        if answer == 'ERROR':
            raise InstrumentError
        return answer



    # 6.4.05 Instrument outputs
    @Feat()
    def x(self):
        """
        Returns x demodulator output in volts or amps, depending on mode
        """
        return self.query('X.')

    @Feat()
    def y(self):
        """
        Returns y demodulator output in volts or amps, depending on mode
        """
        return self.query('Y.')

    @Feat()
    def xy(self):
        """
        Returns x and y demodulator output in volts or amps, depending on mode
        """
        return self.query('XY.')

    @Feat()
    def magnitude(self):
        """
        Returns signal magnitude value in volts or amps, depending on mode
        """
        return self.query('MAG.')

    @Feat()
    def phase(self):
        """
        Returns signal phase in degrees.
        """
        return self.query('PHA.')

    @Feat()
    def mag_phase(self):
        """
        Returns signal magnitude (volts or amps) and phase (degrees).
        """
        return self.query('MP.')

    @Feat()
    def sqrt_noise_spectral_density(self):
        """
        Returns square root of noise spectral density measured at y channel
        output, in V/sqrt(Hz) or A/sqrt(Hz) depending on mode.

        This assumes that the y channel output is Gaussian w/ zero mean.
        """
        return self.query('NHZ.')

    @Feat()
    def equiv_noise_bandwidth(self):
        """
        Returns the equivalent noise bandwidth of the output low pass filter at
        current time constant setting (in Hz)
        """
        return self.query('ENBW.')


    ## 6.4.05 Unimplemented commands:
    # X - fixed point X
    # Y - fixed point Y
    # XY - fixed point XY
    # MAG - fixed point magnitude
    # PHA - fixed point phase
    # MP - fixed point magnitude and phase
    # RT[.] - ratio output
    # LR[.] - log ratio output
    # ENBW - fixed point equivalent noise bandwidth
    # NN - fixed point noise output

    ## Unimplemented user equation functionality
    # DEFEQU - define user equation
    # C1 - user equation C1
    # C2 - user equation C2
    # EQU n - output of equation 1/2

    ## Unimplemented fast setup commands
    # STAR - fast setup command

    # 6.4.01 Signal channel information
    # Should these be implemented as DictFeat?
    @Feat(limits=(0,2,1))
    def imode(self):
        """
        Query current/voltage mode
        Return values correspond to the following table.

        n   Input mode
        0   Current mode off - voltage mode input ENABLED
        1   High bandwidth (HB) current mode enabled
        2   Low noise (LN) current mode enabled
        """
        return self.query('IMODE')

    @imode.setter
    def imode(self, value):
        """
        Current/voltage mode input selector

        n   Input mode
        0   Current mode off - voltage mode input ENABLED
        1   High bandwidth (HB) current mode enabled
        2   Low noise (LN) current mode enabled
        """
        return self.query('IMODE{}'.format(value))

    @Feat(limits=(0, 3,1))
    def vmode(self):
        """
        Query voltage input configuration.

        Value returned corresponds to the following table:
        n   Input configuration
        0:  Both inputs grounded (test mode)
        1:  A input only
        2:  -B input only
        3:  A-B differential mode
        """
        return self.query('VMODE')

    @vmode.setter
    def vmode(self, value):
        """
        Set voltage input configuration according to the following table:

        n   Input configuration
        0:  Both inputs grounded (test mode)
        1:  A input only
        2:  -B input only
        3:  A-B differential mode
        """
        return self.query('VMODE{}'.format(value))

    @Feat(limits=(0,1,1))
    def mode_FET(self):
        """
        Returns voltage mode input device control, with values corresponding
        to the following table:

        0:  Bipolar device, 10 kΩ input impedance, 2 nV/√Hz voltage noise at 1 kHz
        1:  FET, 10 MΩ input impedance, 5 nV/√Hz voltage noise at 1 kHz

        """
        return self.query('FET')

    @mode_FET.setter
    def mode_FET(self, value):
        """
        Sets voltage mode input device control according to following table:

        0:  Bipolar device, 10 kΩ input impedance, 2 nV/√Hz voltage noise at 1 kHz
        1:  FET, 10 MΩ input impedance, 5 nV/√Hz voltage noise at 1 kHz
        """
        return self.query('FET{}'.format(value))

    @Feat(limits=(0,1,1))
    def mode_float(self):
        """
        Queries connector shield switch setting, with returned value corresponding
        to the following table:

        n:  Selection
        0:  Ground
        1:  Float (connected to ground via a 1 kΩ resistor)
        """
        return self.query('FLOAT')

    @mode_float.setter
    def mode_float(self,value):
        """
        Sets connector shield switch setting, with values corresponding to the
        following table:

        n:  Selection
        0:  Ground
        1:  Float (connected to ground via a 1 kΩ resistor)
        """
        return self.query('FLOAT{}'.format(value))

    @Feat(limits=(0,1,1))
    def mode_CP(self):
        """
        Reads out input coupling mode, with return value corresponding to the
        following table:

        n:  Coupling Mode
        0:  AC
        1:  DC
        """
        return self.query('CP')

    @mode_CP.setter
    def mode_CP(self, value):
        """
        Sets input coupling mode according to the following table:

        n:  Coupling Mode
        0:  AC
        1:  DC
        """
        return self.query('CP{}'.format(value))

    @Feat()
    def sensitivity(self):
        """
        Reads the sensitivity in floating point mode. Return value units are
        either volts or amps depending on the IMODE selected.
        """
        return self.query('SEN.')

    @Feat(limits=(0,27,1))
    def sensitivity_n(self):
        """
        Reads the sensitivty according to the following lookup table.
        Note that the physical values change depending on the value of IMODE.

        n   full-scale sensitivity
           IMODE=0  IMODE=1  IMODE=2
        1:    2 nV     2 fA      n/a
        2:    5 nV     5 fA      n/a
        3:   10 nV    10 fA      n/a
        4:   20 nV    20 fA      n/a
        5:   50 nV    50 fA      n/a
        6:  100 nV   100 fA      n/a
        7:  200 nV   200 fA     2 fA
        8:  500 nV   500 fA     5 fA
        9:    1 µV     1 pA    10 fA
        10:   2 µV     2 pA    20 fA
        11:   5 µV     5 pA    50 fA
        12:  10 µV    10 pA   100 fA
        13:  20 µV    20 pA   200 fA
        14:  50 µV    50 pA   500 fA
        15: 100 µV   100 pA     1 pA
        16: 200 µV   200 pA     2 pA
        17: 500 µV   500 pA     5 pA
        18:   1 mV     1 nA    10 pA
        19:   2 mV     2 nA    20 pA
        20:   5 mV     5 nA    50 pA
        21:  10 mV    10 nA   100 pA
        22:  20 mV    20 nA   200 pA
        23:  50 mV    50 nA   500 pA
        24: 100 mV   100 nA     1 nA
        25: 200 mV   200 nA     2 nA
        26: 500 mV   500 nA     5 nA
        27:    1 V     1 µA    10 nA

        """
        return self.query('SEN')

    @sensitivity_n.setter
    def sensitivity_n(self, value):
        """
        Set the sensitivty according to the following lookup table.
        Note that the sensitivity changes depending on the value of IMODE.

        n   full-scale sensitivity
           IMODE=0  IMODE=1  IMODE=2
        1:    2 nV     2 fA      n/a
        2:    5 nV     5 fA      n/a
        3:   10 nV    10 fA      n/a
        4:   20 nV    20 fA      n/a
        5:   50 nV    50 fA      n/a
        6:  100 nV   100 fA      n/a
        7:  200 nV   200 fA     2 fA
        8:  500 nV   500 fA     5 fA
        9:    1 µV     1 pA    10 fA
        10:   2 µV     2 pA    20 fA
        11:   5 µV     5 pA    50 fA
        12:  10 µV    10 pA   100 fA
        13:  20 µV    20 pA   200 fA
        14:  50 µV    50 pA   500 fA
        15: 100 µV   100 pA     1 pA
        16: 200 µV   200 pA     2 pA
        17: 500 µV   500 pA     5 pA
        18:   1 mV     1 nA    10 pA
        19:   2 mV     2 nA    20 pA
        20:   5 mV     5 nA    50 pA
        21:  10 mV    10 nA   100 pA
        22:  20 mV    20 nA   200 pA
        23:  50 mV    50 nA   500 pA
        24: 100 mV   100 nA     1 nA
        25: 200 mV   200 nA     2 nA
        26: 500 mV   500 nA     5 nA
        27:    1 V     1 µA    10 nA

        """
        self.write('TC{}'.format(value))



    @Feat()
    def auto_sensitivity(self):
        """
        The instrument adjusts its full-scale sensitivity so that the magnitude
        output lies between 30% and 90% of full-scale.
        """
        return self.query('AS')

    @Feat()
    def auto_measure(self):
        """
        The instrument adjusts its full-scale sensitivity so that the magnitude
        output lies between 30% and 90% of full-scale, and then performs an
        auto-phase operation to maximize the X channel output and minimize the
        Y channel output.
        """
        return self.query('ASM')

    @Feat(limits=(0,9,1))
    def ac_gain(self):
        """
        Reads out the gain of the signal channel amplifier, in range 0 to 9,
        corresponding to 0dB - 90dB in 10dB steps.
        """
        return self.query('ACGAIN')

    @ac_gain.setter
    def ac_gain(self,value):
        """
        Sets AC gain of signal channel amplifier  in range 0 to 9, corresponding
        to 0dB - 90dB in 10dB steps.
        """
        return self.query('ACGAIN{}'.format(value))

    @Feat(limits=(0,1,1))
    def ac_gain_auto(self):
        """
        Returns if AC Gain is manually or automatically controlled.

        Values correspond to the following table:

        n:  Status
        0:  AC Gain is under manual control
        1:  AC Gain is under automatic control
        """
        return self.query('AUTOMATIC')

    @ac_gain_auto.setter
    def ac_gain_auto(self, value):
        """
        Sets AC gain to manual or automatic based on the following table:

        n:  Status
        0:  AC Gain is under manual control
        1:  AC Gain is under automatic control
        """
        return self.query('AUTOMATIC{}'.format(value))

    # Unimplemented features
    # LF[n1 n2] - signal channel line rejection filter control
    # SAMPLE[n] - main ADC sample rate control
    # RANGE[n] - signal recovery/vector voltmeter mode selector

    # 6.4.02 Reference Channel

    @Feat(limits=(0,2,1))
    def ref_mode(self):
        """
        Returns the instrument reference mode, with return values corresponding
        to the following table:

        n:  Mode
        0:  Single Reference / Virtual Reference mode
        1:  Dual Harmonic mode
        2:  Dual Reference mode
        """
        return self.query('REFMODE')

    @ref_mode.setter
    def ref_mode(self,value):
        """
        Sets the instrument reference mode, according to the following table:

        n:  Mode
        0:  Single Reference / Virtual Reference mode
        1:  Dual Harmonic mode
        2:  Dual Reference mode
        """
        return self.query('REFMODE{}'.format(value))


    @Feat(limits=(0,2,1))
    def ie(self):
        """
        Reads out reference channel source according to the following table:

        n: Selection
        0: INT (internal)
        1: EXT LOGIC (external rear panel TTL input)
        2: EXT (external front panel analog input)
        """
        return self.query('IE')

    @ie.setter
    def ie(self,value):
        """
        Selects reference channel source according to the following table:

        n: Selection
        0: INT (internal)
        1: EXT LOGIC (external rear panel TTL input)
        2: EXT (external front panel analog input)
        """
        return self.query('IE{}'.format(value))

    @Feat(limits=(0,65535,1))
    def refn(self):
        """
        Returns n,measurement harmonic mode

        """
        return self.query('REFN')


    def refn(self, value):
        """


        """
        return self.query('REFN{}'.format(value))

    @Feat(limits=(-360,360))
    def refp(self):
        """
        Sets
        """







    # 6.4.03 Signal Channel Output Filters
    @Feat(units='sec')
    def time_constant(self):
        return self.query('TC.')


    @Feat(limits=(0,29,1))
    def time_constant_n(self):
        return self.query('TC')

    @time_constant_n.setter
    def time_constant_n(self, value):
        """
        Sets lock-in time constant according to the following lookup table:

        0: 10 µs
        1: 20 µs
        2: 40 µs
        3: 80 µs
        4: 160 µs
        5: 320 µs
        6: 640 µs
        7: 5 ms
        8: 10 ms
        9: 20 ms
        10: 50 ms
        11: 100 ms
        12: 200 ms
        13: 500 ms
        14: 1 s
        15: 2 s
        16: 5 s
        17: 10 s
        18: 20 s
        19: 50 s
        20: 100 s
        21: 200 s
        22: 500 s
        23: 1 ks
        24: 2 ks
        25: 5 ks
        26: 10 ks
        27: 20 ks
        28: 50 ks
        29: 100 ks

        """
        self.write('TC{}'.format(value))

    # Unimplemented commands
    # SYNC [n] - synchronous time constant control
    # SLOPE [n] - output low-pass filter slope control


    # 6.4.04 Signal Channel Output Amplifiers
    # TODO implement this

    # 6.4.06 Internal Oscillator
    # TODO implement this

    # 6.4.07 Auxiliary Outputs
    # Not implemeting this section yet
    # Missing commands list:
    # DAC[.]n1[n2] Auxilliary DAC output controls
    # BYTE [n] Digital output port controls

    # 6.4.08 Auxiliary Inputs
    # Not implementing this section yet
    # Missing commands list
    # ADC[.]n - read auxiliary analog-to-digital Inputs
    # ADC3TIME[n] - ADC3 sample time
    # TADC[n] - Auxiliary ADC trigger mode control
    # BURSTTPP [n] - set burst mode time per point rate for ADC1 and ADC2

    # Output Data Curve Buffer
    # Not implementing this section yet
    # Missing commands list:
    # CBD[n] - curve buffer define
    # LEN[n] - curve length control
    # NC - new curve
    # STR[n] - storage interval control
    # TD - take data
    # TDT - take data triggered
    # TDC - take data continually
    # EVENT[n] - event marker control
    # HC - halt curve acquisition
    # M - curve acquisition status monitor
    # DC[.]n - dump acquired curves to computer
    # DCB n - dump acquired curves to computer in binary format
    # DCT n - dump acquired curves to computer in table format

    ## 6.4.10 Computer interfaces (RS232 and GPIB)
    # Not implementing yet
    # Missing functions
    # RS[n1[n2]] - set/read RS232 parameters
    # GP[n1[n2]] - set/read GPIB parameters
    # n1 sets GPIB address in the range 0 to 31
    # n2 sets GPIB terminator and test echo function
    #\N n - Address command for daisy chaining
    # DD[n] - define delimiter control
    # ST - report status byte
    # N - report overload byte
    # MSK - set/read service request mask byte
    # REMOTE[n] - remote only (front panel lock-out) control

    # 6.4.12 Front Panel
    # Not implementing this yet
    # Could be used to auto set up user interface for local operation

    # 6.4.13 Auto Default
    # Not implementing this yet
    # ADF[n] Can be used to reset to factor default settings

    # 6.4.14 Dual Mode Commands
    # Used for either dual reference or dual harmonic modes
    # Check manual to see which channels can be controlled independently

if __name__ == '__main__':

    from lantz import Q_


    #Define units
    volt = Q_(1, 'V')
    sec = Q_(1, 'sec')

    # Define GPIB location
    GPIB_host = 'GPIB0'
    GPIB_address = '10'

    LIA_name = GPIB_host + '::' + GPIB_address + '::INSTR'

    with SignalRecovery7265(LIA_name) as inst:
        print('=== Instrument Identification ===')
        print('idn:{}' .format(inst.idn))
        #print('Firmware revision:{}'.format(inst.firmware_rev))
        print('Firmware version: {}'.format(inst.firmware_ver))


        print('=== Time Constant Settings ===')
        print('Time constant: {}'.format(inst.time_constant))
        inst.time_constant_n = 11
        print('Time constant [n]: {}'.format(inst.time_constant_n))
        inst.time_constant_n = 12




        print('=== Oscillator Settings ===')
        print('Reference in/Ext:')
        print('')




        print('=== Instrument Measurements ===')
        print('X: {}'.format(inst.x))
        print('Y: {}'.format(inst.y))
        print('X,Y: {}'.format(inst.xy))
        print('Magnitude: {}'.format(inst.magnitude))
        print('Phase: {}'.format(inst.phase))
        print('Magnitude, Phase: {}'.format(inst.mag_phase))
        print('Sqrt(Noise Spectral Density): {}'.format(inst.sqrt_noise_spectral_density))
        print('Equivalent Noise Bandwidth: {}'.format(inst.equiv_noise_bandwidth))
