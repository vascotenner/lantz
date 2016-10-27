

from lantz import Feat, DictFeat, Action
from lantz.errors import InstrumentError
from lantz.messagebased import MessageBasedDriver

from time import sleep

class ITC4020(MessageBasedDriver):


    DEFAULTS = {
        'COMMON': {
            'write_termination': '\n',
            'read_termination': '\n'
        }
    }

    COM_DELAY = 0.2

    def write(self, *args, **kwargs):
        super().write(*args, **kwargs)
        sleep(self.COM_DELAY)
        return

    @Feat(read_once=True)
    def idn(self):
        return self.query('*IDN?')

    @Feat()
    def key_locked(self):
        return bool(int(self.query('OUTP:PROT:KEYL:TRIP?')))

    @Feat(values={'C': 'CEL', 'F': 'FAR', 'K': 'K'})
    def temperature_unit(self):
        self.t_unit = self.query('UNIT:TEMP?')
        return self.t_unit

    @temperature_unit.setter
    def temperature_unit(self, value):
        self.write('UNIT:TEMP {}'.format(value))

    @Feat()
    def temperature(self):
        return float(self.query('MEAS:SCAL:TEMP?'))

    @Feat()
    def temperature_setpoint(self):
        return float(self.query('SOUR2:TEMP?'))

    @Action()
    def read_error_queue(self):
        no_error = "+0,'No error'"
        error = inst.query('SYST:ERR:NEXT?')
        while(error != no_error):
            print(error)
            error = inst.query('SYST:ERR:NEXT?')


    @Feat(values={False: '0', True: '1'})
    def ld_state(self):
        return self.query('OUTP1:STAT?')

    @ld_state.setter
    def ld_state(self, value):
        self.write('OUTP1:STAT {}'.format(value))

    @Feat(units='A')
    def ld_current_setpoint(self):
        return float(self.query('SOUR:CURR?'))

    @Feat(units='A', limits=(0.0, 1.0))
    def ld_current(self):
        return float(self.query('MEAS:CURR?'))

    @ld_current.setter
    def ld_current(self, value):
        inst.write('SOUR:CURR {:.5f}'.format(value))

    @DictFeat(units='W', keys={'photodiode', 'pd', 'thermopile', 'tp', 'power meter'})
    def ld_power(self, method):
        query = 'MEAS:POW{}?'
        ml = method.lower()
        if ml in {'photodiode', 'pd'}:
            method_val = 2
        elif ml in {'thermopile', 'tp', 'power meter'}:
            method_val = 3
        return float(self.query(query.format(method_val)))

    @Feat(values={False: '0', True: '1'})
    def tec_state(self):
        return self.query('OUTP2:STAT?')

    @tec_state.setter
    def tec_state(self, value):
        self.write('OUTP2:STAT {}'.format(value))




    @Action()
    def turn_on_seq(self, temp_error=0.05, current_error=0.005):
        if self.output_state:
            print("Laser is already ON!")
            return

        #Turn ON sequence:
        #   1. TEC ON
        #   2. Wait for temperature == set_temperature
        #   3. LD ON
        #   4. Wait for current == set_current

        # 1. TEC ON
        self.write('OUTP2:STAT ON')

        # 2. Wait
        setpoint = self.temperature_setpoint
        while(abs(setpoint-self.temperature)>temp_error):pass


        # 3. LD ON
        self.write('OUTP1:STAT ON')

        # 4. Wait
        setpoint = self.LD_current_setpoint
        while(abs(setpoint-self.LD_current)>current_error):pass

    @Action()
    def turn_off_seq(self, current_error=0.005):
        #Turn OFF sequence:
        #   1. LD OFF
        #   2. Wait for current == 0
        #   3. TEC OFF

        # 1. LD OFF
        self.write('OUTP1:STAT OFF')

        # 2. Wait
        while(abs(self.LD_current)>current_error):pass

        # 1. TEC OFF
        self.write('OUTP2:STAT OFF')



if __name__ == '__main__':
    import logging
    import sys
    from lantz.log import log_to_screen
    log_to_screen(logging.CRITICAL)
    res_name = sys.argv[1]
    fmt_str = "{:<30}|{:>30}"
    on_time = 20
    with ITC4020(res_name) as inst:
        print(fmt_str.format("Temperature unit", inst.temperature_unit))
        print(fmt_str.format("Device name", inst.query('*IDN?')))
        print(fmt_str.format("LD state", inst.ld_state))
        print(fmt_str.format("TEC state", inst.tec_state))
        print("Turning on TEC and LD...")
        inst.tec_state = True
        inst.ld_state = True
        print(fmt_str.format("LD power (via photodiode)", inst.ld_power['pd']))
        print(fmt_str.format("LD power (via thermopile)", inst.ld_power['tp']))
        print(fmt_str.format("LD state", inst.ld_state))
        print(fmt_str.format("TEC state", inst.tec_state))
        print(fmt_str.format("LD temperature", inst.temperature))
        print(fmt_str.format("LD power (via photodiode)", inst.ld_power['pd']))
        print(fmt_str.format("LD power (via thermopile)", inst.ld_power['tp']))
        sleep(on_time)
        print("Turning off TEC and LD...")
        inst.tec_state = False
        inst.ld_state = False
        print(fmt_str.format("LD state", inst.ld_state))
        print(fmt_str.format("TEC state", inst.tec_state))
