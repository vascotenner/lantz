# -*- coding: utf-8 -*-
"""
    lantz.drivers.newport.agilis
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation of Agilis UC8/UC2 piezo controller

    Authors: Kevin Miao, Alexandre Bourassa
    Date: 12/14/2015

"""

from lantz import Action, Feat
from lantz.messagebased import MessageBasedDriver

from pyvisa.constants import Parity, StopBits

import time

class Agilis(MessageBasedDriver):

    DEFAULTS = {
        'ASRL': {
            'write_termination': '\r\n',
            'read_termination': '\r\n',
            'baud_rate': 921600,
            'parity': Parity.none,
            'stop_bits': StopBits.one,
            'timeout': None,
        }
    }

    # We need a synchronous decorator (or something to slow down function calls)
    # most commands need ~1s to complete, while select commands may need up to
    # 2 minutes

    @Action()
    def reset(self):
        """
        Reset controller
        """
        self.write('RS')
        return

    #@Feat(values={1, 2, 3, 4})
    @Feat()
    def channel(self):
        return self.query('CC?')

    @channel.setter
    def channel(self, value):
        """
        Set channel
        """
        self.write('CC{}'.format(value))

    @Feat()
    def delay(self, axis):
        return self.query('{}DL?'.format(axis))

    @delay.setter
    def delay(self, axis, value):
        self.write('{}DL{}'.format(axis, value))

    @Feat()
    def jog(self, axis):
        return self.query('{}JA?'.format(axis))

    @Action()
    def jog(self, axis, value):
        self.write('{}JA{}'.format(axis, value))

    @Action()
    def measure_position(self, axis):
        return self.query('{}MA'.format(axis))

    @Action()
    def move_to_limit(self, axis, value):
        self.write('{}MV{}'.format(axis, value))

    @Action()
    def move(self, axis, value, mode):
        raise NotImplementedError

    @Feat()
    def limit_status(self):
        return self.query('PH')

    @Action()
    def stop(self, axis):
        self.write('{}ST'.format(axis))

    @Feat()
    def version(self):
        return self.query('VE')

    @mode.setter
    def mode(self, value):
        raise NotImplementedError
