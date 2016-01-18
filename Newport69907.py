from lantz import Feat, Action
from lantz.messagebased import MessageBasedDriver
from time import sleep


class Newport69907(MessageBasedDriver):
    """
    This class implements serial control of a Newport69907 arc lamp power
    supply.
    """
    DEFAULTS = {'ASRL': {'write_termination': '\r',
                         'read_termination': '',
                         'baud_rate': 9600,
                         'data_bits': 8,
                         'parity': constants.Parity.none,
                         'stop_bits': constants.StopBits.one,
                         'encoding': 'latin-1',
                         'timeout': 10000}}

    max_lamp_amps = 3  # amps
    max_lamp_power = 100  # watts

    def parse_status_register(self, status_register):
        """
        Parses the status registry codes bit by bit into meaningful statement.
        These error bits correspond to whether or not the corresponding LEDs
        on the front panel are illuminated.

        Bit 7 - Lamp on
        Bit 6 - Ext
        Bit 5 - Power/Current mode
        Bit 4 - Cal mode
        Bit 3 - Fault
        Bit 2 - Communication
        Bit 1 - Limit
        Bit 0 - Interlock
        """
        status_code = int(('0x' + error_register.replace('STB', '')), 16)
        print('Status code:{}'.format(status_code))
        if status_code > 128:
            print('Status: Lamp on')
            status_code -= 128
        if status_code > 64:
            print('Status: Ext')
            status_code -= 64
        if status_code > 32:
            print('Status: Power Mode')
            status_code -= 32
        else:
            print('Status: Current Mode')
        if status_code > 16:
            print('Status: Cal Mode')
            status_code -= 16
        if status_code > 8:
            print('Status: Fault')
            status_code -= 8
        if status_code > 4:
            print('Status: Comm')
            status_code -= 4
        if status_code > 2:
            print('Status: Limit')
            status_code -= 2
        if status_code > 1:
            print('Status: Interlock')
        return 0

    def parse_error_register(self, error_register):
        """
        Parses the status registry codes bit by bit into meaningful statement.

        Bit 7 - Power on
        Bit 6 - User request
        Bit 5 - Command error
        Bit 4 - Execution error
        Bit 3 - Device dependent error
        Bit 2 - Query error
        Bit 1 - Request control
        Bit 0 - Operation complete
        """
        # convert hex string into integer
        err_code = int(('0x' + error_register.replace('ESR', '')), 16)
        print('error code')
        if err_code > 128:
            print('Error: Power on')
            err_code -= 128
        if err_code > 64:
            print('Error: User request')
            err_code -= 64
        if err_code > 32:
            print('Error: Command error')
            err_code -= 32
        if err_code > 16:
            print('Error: Execution error')
            err_code -= 16
        if err_code > 8:
            print('Error: Device dependent error.')
            err_code -= 8
        if err_code > 4:
            print('Error: Query error.')
            err_code -= 4
        if err_code > 2:
            print('Error: Request control')
            err_code -= 2
        if err_code > 1:
            print('Error: Operation complete')
        return 0

    @Feat()
    def idn(self):
        """
        Return power supply model number
        """
        return self.query('IDN?')

    @Feat()
    def status(self):
        """
        Returns status information of the instrument.
        """
        status = self.query('STB?')
        self.parse_status_register(status)

    @Feat()
    def error_status(self):
        """
        Returns the instrument error status.
        """
        error_register = self.query('ESR?')
        self.parse_error_register(error_register)

    @Feat()
    def amps(self):
        """
        Returns output amperage displayed on the front panel.
        """
        return float(self.query('AMPS?'))

    @Feat()
    def volts(self):
        """
        Return output voltage displayed on front panel.
        """
        return float(self.query('VOLTS?'))

    @Feat()
    def watts(self):
        """
        Returns output wattage displayed on front panel.
        """
        return int(self.query('WATTS?'))

    @Feat()
    def lamp_hrs(self):
        """
        Returns the number of hours on the current lamp.
        """
        return int(self.query('LAMP\sHRS'))

    @Feat()
    def amp_preset(self):
        """
        Returns the lamp amperage preset value.
        """
        return float(self.query('A-PRESET?'))

    @amp_preset.setter
    def amp_preset(self, preset_val):
        """
        Sets the lamp amperage preset value to preset_val.
        """
        error_status = self.query('A-PRESET={0:.1f}'.format(preset_val))
        return self.parse_error_register(error_status)

    @Feat()
    def power_preset(self):
        """
        Returns the lamp power preset value (in watts).
        """
        return = int(self.query('P-PRESET?'))

    @power_preset.setter
    def power_preset(self, power_preset):
        """
        Sets the lamp powr preset value (in watts).
        """
        error_status = self.query('P-PRESET={}'.format(ceil(power_preset)))
        return self.parse_error_register(error_status)

    @Feat(limits=(0, max_lamp_amps))
    def amp_lim(self):
        """
        Return current lamp amperage limit.
        """
        return float(self.query('A-LIM?'))

    @amp_lim.setter
    def amp_lim(self, max_amps):
        """
        Sets current amperage limit to max_amps
        """
        error_register = self.query('A-LIM={0:.1f}')

    @Feat(limits=(0, max_lamp_power))
    def power_lim(self):
        """
        Return current power limit.
        """
        return int(self.query('P-LIM?'))

    @power_lim.setter
    def power_lim(self, max_power):
        """
        Sets the power limit of the lamp to max_power.
        """
        error_register = self.query('P-LIM={}'.format(floor(max_power)))

    @Action()
    def start_lamp(self):
        """
        Turns on the arc lamp.
        """
        error_register = self.query('START')

    @Action()
    def stop_lamp(self):
        """
        Turns off the arc lamp.
        """
        error_register = self.query('STOP')

    @Action()
    def reset(self):
        """
        Returns the arc lamp to factory default settings.
        """
        error_register = self.query('RST')


if __name__ == '__main__':
    with Newport69907('ASRL10::INSTR') as inst:
        print('Serial number:{}'.format(inst.idn))
        print('Status:{}'.format(inst.status))

        # TODO: add more commands here.
