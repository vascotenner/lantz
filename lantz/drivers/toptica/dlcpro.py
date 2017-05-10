# -*- coding: utf-8 -*-
"""
    lantz.drivers.toptica.dlcpro.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation of Toptica DLC-pro laser controller

    Author: Alexandre Bourassa
    Date: 21/04/2017
"""

import numpy as np
from lantz import Action, Feat, DictFeat, ureg
from lantz.messagebased import MessageBasedDriver

class DLC(MessageBasedDriver):

        DEFAULTS = {
            'COMMON': {
                'write_termination': '\n',
                'read_termination': '\n',
            }
        }
        def initialize(self):
            super().initialize()
            ## Clear the welcome message
            for i in range(5): print(self.resource.read_raw())
            self._read = self.read
            self.read  = self.parsed_read

        def parsed_read(self, *args, **kwargs):
            ans = self._read(*args, **kwargs)
            if ans[0] == '>': # Take away the prompt "> "
                ans = ans[2:]
            return ans.strip('"') # Take away the quotation for strings

        def get(self, param):
            return self.query("(param-ref '{})".format(param))

        def set(self, param, val):
            err = self.query("(param-set! '{} {})".format(param, val))
            if err != '0':
                raise Exception("(param-set! '{} {}) returned an error code of '{}'".format(param, val, err))
            return err

        @Feat
        def idn(self):
            """
            Returns DLCpro
            """
            return self.get("system-type")


        @Feat(values={True: '#t', False: '#f'})
        def output(self):
            return self.get('laser1:dl:cc:enabled')

        @output.setter
        def output(self, val):
            return self.set('laser1:dl:cc:enabled', val)


        @Feat(values={True: '#t', False: '#f'})
        def piezo_enabled(self):
            return self.get('laser1:dl:pc:enabled')

        @piezo_enabled.setter
        def piezo_enabled(self, val):
            return self.set('laser1:dl:pc:enabled', val)


        @Feat(units='V')
        def piezo_vmax(self):
            return self.get('laser1:dl:pc:voltage-max')

        @piezo_vmax.setter
        def piezo_vmax(self, val):
            return self.set('laser1:dl:pc:voltage-max', val)


        @Feat(units='V')
        def piezo_vmin(self):
            return self.get('laser1:dl:pc:voltage-min')


        @Feat(units='V')
        def piezo_vset(self):
            return self.get('laser1:dl:pc:voltage-set')

        @piezo_vset.setter
        def piezo_vset(self, val):
            return self.set('laser1:dl:pc:voltage-set', val)






