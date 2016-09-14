"""
    lantz.drivers.tektronix.awg5000
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Drivers for the Tektronix 5000 series AWG

    Authors: Alexandre Bourassa, Kevin Miao
    Date: September 14, 2016
"""

import numpy as np
import re
from enum import Enum

from lantz.messagebased import MessageBasedDriver
from lantz import Feat, DictFeat, Action


class AWGState(Enum):
    stopped = 0
    trigger_wait = 1
    running = 2


class AWG5000(MessageBasedDriver):

    DEFAULTS = {
        'COMMON': {
            'write_termination': '\r\n',
            'read_termination': '\r\n',
        },
    }

    def __init__(self, resource_name, *args, **kwargs):
        super().__init__(resource_name, *args, **kwargs)
        self.ip = re.findall('[0-9]+.[0-9]+.[0-9]+.[0-9]+', resource_name)
        return

    @Feat(read_once=True)
    def idn(self):
        return self.query('*IDN?')

    @Feat()
    def toggle_run(self):
        return AWGState(int(self.query('AWGC:RST?')))

    @toggle_run.setter
    def toggle_run(self, state):
        if state or state == AWGState.running:
            cmd = 'RUN'
        elif not state or state == AWGState.stopped:
            cmd = 'STOP'
        else:
            raise ValueError('invalid run state: {}'.format(state))
        self.write('AWGC:{}:IMM'.format(cmd))

    @DictFeat(values={True: '1', False: '0'})
    def toggle_output(self, channel):
        return self.query('OUTP{}:STAT?'.format(channel))

    @toggle_output.setter
    def toggle_output(self, channel, state):
        self.write('OUTP{}:STAT {}'.format(channel, state))

    @Action()
    def toggle_all_outputs(self, state):
        for channel in range(1, 5):
            self.toggle_output[channel] = state

    @Action()
    def jump_to_line(self, line):
        self.write('SEQ:JUMP:IMM {}'.format(line))

    @Action()
    def trigger(self):
        self.write('*TRG')

    @DictFeat()
    def waveform(self, key):
        index, channel = key
        return self.query('SEQ:ELEM{}:WAV{}?'.format(index, channel))

    @waveform.setter
    def waveform(self, key, value):
        index, channel = key
        self.write('SEQ:ELEM{}:WAV{} {}'.format(index, channel, value))


if __name__ == '__main__':
    test()
