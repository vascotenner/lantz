# -*- coding: utf-8 -*-
from lantz.messagebased import MessageBasedDriver
from lantz import Feat
import time
#from lantz.drivers.coherent.fieldmastergs import FieldMasterGS

class PilotBox(MessageBasedDriver):

    DEFAULTS = {
        'COMMON': {
            'read_termination': '\r\n',
            'write_termination': '\r',
        },
    }

    # def initialize(self):
    #     print("turning off this goddamn echo shit...")
    #     self.write('system:echo off')


    @Feat(read_once=True)
    def idn(self):
        return self.query('*idn?')

    @Feat(read_once=True)
    def echo(self):
        return self.query('system:echo off')

    @Feat(read_once=True)
    def min(self):
        print(self.query(':Laser:ILIMit? MIN'))
        return float(self.query(':Laser:ILIMit? MIN'))


    @Feat(read_once=True)
    def max(self):
        return float(self.query(':Laser:ILIMit? MAX'))


    @Feat(read_once=True, values={'Current': 'I', 'Power': 'P'})
    def laser_mode(self):
        mode = self.query(':Laser:MODe?')
        return mode[0]
    @laser_mode.setter
    def laser_mode(self, mode):
        self.write(':Laser:MODe {}'.format(mode))


    @Feat(read_once=True)
    def current_meas(self):
        return self.query(':Laser:CURRent?')


    @Feat(read_once=True)
    def current_set(self):
        return self.query(':Laser:CURRent:Set?')
    @current_set.setter
    def current_set(self, current):
        self.write(':Laser:CURRent {}A'.format(current))


    @Feat(read_once=True)
    def laser_status(self):
        return self.query(':Laser:STATus?')
    @laser_status.setter
    def laser_status(self, status):
        self.write(':Laser:STATus {}'.format(status))


import time
if __name__ == '__main__':
    s = PilotBox('COM9')
    with s as pbox:
        #pbox.initialize()
        print(pbox.idn)
        print(pbox.echo)
        print(pbox.min)
        print(pbox.max)
        #print(pbox.laser_mode)
        #pbox.laser_mode = 'Current'
        #print(pbox.laser_mode)
        #print(pbox.current_meas)

        #time.sleep(7)
        pbox.current_set = 0.3435


        # print('ok')
        # time.sleep(3)
        # pbox.current_set = 0.1900
        # print('ok')
        # time.sleep(3)
        # pbox.current_set = 0.1950
        # print('ok')
        # time.sleep(3)
        # pbox.current_set = 0.2000
        # print('ok')
        # time.sleep(3)
        # pbox.current_set = 0.2050
        # print('ok')
        # time.sleep(3)
        # pbox.current_set = 0.2100



        #print(pbox.current_set)
        #print(pbox.current_meas)
        print('')
        #print(pbox.laser_status)
        #pbox.laser_status = 'ON'
        #time.sleep(5)
        #print(pbox.laser_status)
        #print(pbox.current_meas)
        #pbox.laser_status = 'OFF'
        #time.sleep(1)
        print(pbox.laser_status)
        print(pbox.current_set)
        print(pbox.current_meas)



"""
For some reason the actual measured laser current is always zero
Maybe the detector is broken or something
"""



#
