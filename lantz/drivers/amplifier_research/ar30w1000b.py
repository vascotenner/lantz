"""
    lantz.drivers.amplifier_research.ar30w1000b
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation of 30W1000B RF amplifier

    Author: Thomas Kiely
    Date: 6/21/2016
"""

import numpy as np
from lantz import Action, Feat, DictFeat, ureg
from lantz.messagebased import MessageBasedDriver

class AR30W1000B(MessageBasedDriver):
    
        DEFAULTS = {
            'COMMON': {
                'write_termination': '\r\n',
                'read_termination': '\n',
            }
        }
        
        @Action()
        def power_on(self):
            self.write('P1')
        
        @Action()
        def power_off(self):
            self.write('P0')
        
        @Feat()
        def gain(self):
            """
            sets gain from 0 (min) to 4095 (max)
            this range encompasses a minimum of 10dB
            the maximum value of this range is at least 44dB
            """
            return int(self.query('G?')[1:])
        
        @gain.setter
        def gain(self,value):
            stringValue = '{0:0=4d}'.format(value)
            self.write('G{:s}'.format(stringValue))
        
        @Action()
        def reset(self):
            """
            resets device, clearing all faults, if possible
            """
            self.write('R')