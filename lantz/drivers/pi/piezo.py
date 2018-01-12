"""
    lantz.drivers.pi.piezo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Implements the drivers to control pi piezo motion controller 
    via serial. It uses the PI General Command Set.
    
    For USB, one first have to install the windows driver from PI.
    :copyright: 2017, see AUTHORS for more details.
    :license: GPL, see LICENSE for more details.
    
    Todo: via network?
    Source: Instruction Manual (PI)
"""

from lantz.feat import Feat
from lantz.action import Action
#from lantz.serial import SerialDriver
from lantz.messagebased import MessageBasedDriver
from pyvisa import constants
#from lantz.visa import GPIBVisaDriver
from lantz import Q_, ureg
from lantz.processors import convert_to
import time
import numpy as np
import copy

#TODO
#Replace all send with write and remove \n
#Ask for errors often

def to_int(val):
    if not is_numeric(val):
        val = val.strip()
        if val == '':
            val = 0
    return int(val)

def to_float(val):
    if not is_numeric(val):
        val = val.strip()
        if val == '':
            val = 0
    return float(val)

class Piezo(MessageBasedDriver):
    """ PI piezo motion controller. It assumes all axes to have units um
    
    Params:
    axis: axis number to controll"""

    DEFAULTS = {
                'COMMON': {'write_termination': '\r\n',
                    'read_termination': '\r\n',},
# TODO: set via PI software
#                'ASRL':{
#                    'timeout': 4000, #ms
#                    'encoding': 'ascii',
#                    'data_bits': 8,
#                    'baud_rate': 19200,
#                    'parity': constants.Parity.none,
#                    'stop_bits': constants.StopBits.one,
#                    'flow_control': constants.VI_ASRL_FLOW_RTS_CTS,#constants.VI_ASRL_FLOW_NONE,
#                    },
                }

    def initialize(self, axis=1, sleeptime_after_move=0*ureg.ms):
        super().initialize()
        self.axis = 1
        self.sleeptime_after_move = sleep_after_move
        
    def recv_numeric(self,length):
        try:
            message = self.stage.recv(length)
        except (socket.timeout, socket.error), error:
            print 'Stage not responsive! ', error
            if self.stayconnected:
                self.retries = self.retries + 1
                if self.retries < 10:
                    print 'Retry to connect %i/%i' % (self.retries, 10)
                    self.connect()
                else:
                    print 'To many retries. Not connected to socket'
                    self.retries = 0
            message = ''
        message = message.strip()
        if message == '':
            message = 0
        return message
    
    @Action()
    def errors(self):
        error = int(self.query('ERR?'))
        if self.error != 0:
            self.log_error('Stage error: code {}'.format(self.error))
        return self.error
    
    @Feat()
    def idn(self):
        self.stage.send("*IDN?\n")
        idn = self.recv(256)
        return idn
        
    @Action()
    def stop():
        '''Stop all motions'''
        self.servo = False
        self.write("#24")
        
    def finalize(self):
        """ Disconnects stage """
        self.stop()
        super().finalize()
            
    @Feat(values={True: '1', False: '0'})
    def servo(self, state):
        ''' Set the stage control in open- or closed-loop (state = False or True)'''
        return to_int(self.query('SVO?')
        
    @serco.setter
    def servo(self, state):
        self.send('SVO 1 %d\n' % state)

    @Feat(units='um/s')
    def velocity(self):
        ''' Set the stage velocity (closed-loop only)'''
        return self.query('VEL?')
   
    @velocity.setter
    def velocity(self, velocity):
        return self.write('VEL 1 %f' % velocity)

    @Feat(units='um'):
    def position(self):
        ''' Move to an absolute position the stage (closed-loop only)'''
        return self.query('POS?')

    @position.setter
    def position(self, position):
        self.move_to(position)

    @Action(units=('um','ms'))
    def move_to(self, position, timeout=None):
        ''' Move to an absolute position the stage (closed-loop only)'''
        ret = self.write('MOV %i %f' % self.axis, position)
        timeout = self.sleeptime_after_move if timeout is None:
        time.sleep(timeout.to('s')) # Give the stage time to move! (in seconds!)
        return ret
        
    @Feat(units='um'):
    def read_stage_position(self, nr_avg = 1):
        ''' Read the current position from the stage'''
        positions = [self.position for n in nr_avg]
        return np.avg(positions)

# before operating, ensure that the notch filters are set to the right frequencies. These frequencies depend on the load on the piezo, and can be determined in NanoCapture.
if __name__=='__main__':
    stage = Piezo('')
    stage.sleeptime_after_move = 15*ureg.ms
    
    time.sleep(1)

    stage.servo = True
    time.sleep(1)
    stage.velocity = 0.5*ureg.um/ureg.s

    stage.position = 0
    print 'stage position measured: ', stage.position

    steps = 200
    stepsize = 100.0*ureg.nm
    for n in range(steps):
        stage.position = n*stepsize
        print 'stage position measured: ', stage.position
