# -*- coding: utf-8 -*-
"""
    lantz.drivers.lakeshore.temperature336
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Driver for temperature controller mode 336

    :copyright: 2015 by Lantz Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import sys
sys.path.append('R:\qo\tenner\tmp\lantz_vasco')
from lantz import Feat
from lantz.messagebased import MessageBasedDriver

class Temperature336(MessageBasedDriver):

    DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n',
                          }}


    @Feat(units='K')
    def temperature(self):
        """Phase shift of the reference.
        """
        return self.query('KRDG?')

if __name__ == '__main__':
    from lantz.ui.qtwidgets import start_test_app

    with Temperature336('COM4') as inst:
        start_test_app(inst)

