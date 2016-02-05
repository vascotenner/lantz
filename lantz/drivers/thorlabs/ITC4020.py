

from lantz import Feat, DictFeat, Action
from lantz.errors import InstrumentError
from lantz.messagebased import MessageBasedDriver

from time import sleep

class ITC4020(MessageBasedDriver):


    DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}

    COM_delay = 0.2

    def write(self, *args, **kwargs):
        super(ITC4020, self).write(*args, **kwargs)
        sleep(self.COM_delay)

    @Feat(read_once=True)
    def idn(self):
        return self.query('*IDN?')

    @Feat
    def key_locked(self):
        return bool(int(self.query("OUTP:PROT:KEYL:TRIP?")))

    @Feat
    def temperature(self):
        return float(self.query("MEAS:SCAL:TEMP?"))

    @Feat
    def temperature_setpoint(self):
        return float(self.query("SOUR2:TEMP?"))

    @Feat
    def LD_current_setpoint(self):
        return float(self.query("SOUR:CURR?"))

    @Feat(limits=(0,1))
    def LD_current(self):
        return float(self.query("MEAS:CURR?"))

    @LD_current.setter
    def LD_current(self, value):
        inst.write("SOUR:CURR {:.5f}".format(value))

    @Feat
    def output_state(self):
        return bool(int(self.query("OUTP:STAT?")))

    @Feat
    def PD_power(self):
        return float(self.query("MEAS:POW2?"))

    @Action()
    def read_error_queue(self):
        no_error = '+0,"No error"'
        error = inst.query("SYST:ERR:NEXT?")
        while(error != no_error):
            print(error)
            error = inst.query("SYST:ERR:NEXT?")

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
        self.write("OUTP2:STAT ON")

        # 2. Wait
        setpoint = self.temperature_setpoint
        while(abs(setpoint-self.temperature)>temp_error):pass


        # 3. LD ON
        self.write("OUTP1:STAT ON")

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
        self.write("OUTP1:STAT OFF")

        # 2. Wait
        while(abs(self.LD_current)>current_error):pass

        # 1. TEC OFF
        self.write("OUTP2:STAT OFF")



if __name__ == '__main__':
    inst = ITC4020('USB0::0x1313::0x804A::M00336070::INSTR')
    inst.initialize()
    print(inst.query('*IDN?'))
