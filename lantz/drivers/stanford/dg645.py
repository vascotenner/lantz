# -*- coding: utf-8 -*-
"""
    lantz.drivers.stanford.dg645
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Implementation of DG645 digital delay generator
    Author: Kevin Miao
    Date: 1/14/2016
"""

from enum import IntEnum

from lantz import Action, Feat, DictFeat, Q_
from lantz.messagebased import MessageBasedDriver

class DG645(MessageBasedDriver):

    DEFAULTS = {
        'COMMON': {
            'write_termination': '\r\n',
            'read_termination': '\r\n',
        }
    }

    class Channel(IntEnum):

        T0 = 0
        T1 = 1
        A = 2
        B = 3
        C = 4
        D = 5
        E = 6
        F = 7
        G = 8
        H = 9

    @Feat()
    def idn(self):
        return self.query('*IDN?')

    @Action()
    def reset(self):
        self.write('*RST')

    @DictFeat()
    def delay(self, channel):
        if channel not in self.Channel:
            raise ValueError('invalid channel: {}'.format(channel))
        retval = self.query('DLAY? {}'.format(channel))
        linked, offset = retval.split(',')
        return self.Channel(int(linked)), float(offset)

    @delay.setter
    def delay(self, channel, value):
        if channel not in self.Channel:
            raise ValueError('invalid channel: {}'.format(channel))
        try:
            linked, offset = value
        except TypeError:
            raise TypeError('delay value must be tuple (linked, delay)')
        args = channel, linked.value, offset
        self.write('DLAY {},{:d},{:1.12e}'.format(*args))
        err = int(self.query('LERR?'))
        if not err:
            return
        elif err == 10:
            raise ValueError('Illegal value: a parameter was out of range')
        elif err == 12:
            raise ValueError('Illegal delay: the requested delay is out of range')
        elif err == 13:
            raise ValueError('Illegal link: the requested delay linkage is illegal')
        else:
            raise ValueError('Error code {:d}; refer to DG645 error codes')
        return

    @Feat(limits=(1, 2 ** 32 - 1))
    def burst_count(self):
        return self.query('BURC?')

    @burst_count.setter
    def burst_count(self, value):
        self.write('BURC {:d}'.format(value))

    @Feat(units='s')
    def burst_delay(self):
        return self.query('BURD?')

    @burst_delay.setter
    def burst_delay(self, value):
        self.write('BURD {:1.12e}'.format(value))

    @Feat(values={True: '1', False: '0'})
    def burst_mode(self):
        return self.query('BURM?')

    @burst_mode.setter
    def burst_mode(self, value):
        self.write('BURM {:s}'.format(value))

    @Feat(units='s', limits=(100e-9, (2 ** 32 - 1) * 1e-8, 10e-9))
    def burst_period(self):
        return self.query('BURP?')

    @burst_period.setter
    def burst_period(self, value):
        self.write('BURP {:1.12e}')

    @Feat(values={True: '1', False: '0'})
    def burst_config(self):
        return self.query('BURT?')

    @burst_config.setter
    def burst_config(self, value):
        self.write('BURT {:s}'.format(value))
