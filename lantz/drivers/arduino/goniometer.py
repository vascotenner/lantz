# -*- coding: utf-8 -*-
"""
    lantz.drivers.arduino.goniometer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lantz interface to the arduino controlling the goniometer

    Authors: Alexandre Bourassa
    Date: 3/28/2017

"""

from lantz import Action, Feat, DictFeat
from lantz.messagebased import MessageBasedDriver

from pyvisa.constants import Parity, StopBits

import time

class Goniometer(MessageBasedDriver):

    comm_delay = 1

    DEFAULTS = {
        'ASRL': {
            'write_termination': '\n',
            'read_termination': '\r\n',
            'baud_rate': 9600,
            'timeout': None,
        }
    }

    errors = {
     -1:  'tetha or phi were out of bounds',
     -2:  'alpha or beta were out of bounds',
     -3:  'attempted rotateTo while run_state != 0',
     -4:  'period is out of bound',
    -10:  'Unknown cmd',
    -11:  'other error',
    -50:  'no error',
    }

    def check_error(self, err):
        if type(err) == int and err<0:
            if err != -50:
                raise Exception(self.errors[int(err)])
            else:
                print("No Error")

    def write_and_check(self, *args, **kwargs):
        self.check_error(self.query(*args, **kwargs))

    def query(self, cmd):
        super().write(cmd)
        time.sleep(self.comm_delay)
        ans = super().read()
        self.check_error(ans)
        ans = super().read()
        return ans

    @Feat()
    def theta(self):
        return self.query('theta?')

    @theta.setter
    def theta(self, val):
        self.query('theta {}'.format(val))

    @Feat()
    def phi(self):
        return self.query('phi?')

    @phi.setter
    def theta(self, val):
        self.query('phi {}'.format(val))


    @Action()
    def zero(self):
        self.write('zero 0')
        self.write('zero 1')

    @Feat()
    def state(self):
        return self.query('state?')

    @Action()
    def stop(self):
        self.write('stop')
