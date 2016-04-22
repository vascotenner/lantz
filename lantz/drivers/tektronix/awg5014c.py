"""
    lantz.drivers.tektronix.awg5014c
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Drivers for the AWG5014C using RAW SOCKETS

    Authors: Alexandre Bourassa
    Date: 20/04/2016
"""
import numpy as _np

from lantz import Feat, DictFeat, Action
from lantz.feat import MISSING
from lantz.errors import InstrumentError
from lantz.messagebased import MessageBasedDriver

from spyre.Tools.wfm_writer import iee_block_to_array, array_to_iee_block

class AWG5014C(MessageBasedDriver):
    """E8364B Network Analyzer
    """

    DEFAULTS = {'COMMON': {'write_termination': '\r\n',
                           'read_termination': '\r\n'}}

    @Feat(read_once=True)
    def idn(self):
        return self.query('*IDN?')

    @Action()
    def get_waveform_data(self, name):
        self.write('WLIS:WAV:DATA? "{}"'.format(name))
        data = self.resource.read_raw()
        return iee_block_to_array(data)

    @Action()
    def set_waveform_data(self, name, analog, marker1, marker2, start_index=None, size=None):
        """ Sets the data for waveform <name>.
            analog should be an array of float and marker 1 and 2 an array of bool or 0/1
            analog, marker1 and marker2 should have the same dimensions
        """
        data = array_to_iee_block(analog, marker1, marker2)
        cmd = bytes('WLIS:WAV:DATA "{}",'.format(name), encoding='ascii')
        if not start_index is None:
            cmd += bytes('{},'.format(start_index), encoding='ascii')
            if not size is None:
                cmd += bytes('{},'.format(size), encoding='ascii')
        term = bytes(self.resource.write_termination, encoding='ascii')

        cmd += data + term
        self.log_debug('Writing {!r}', cmd)
        self.resource.write_raw(cmd+data+term)

    @Action()
    def create_new_waveform(self, name, size, type='REAL'):
        """ Create a new waveform with a given name and size (in number of points).
            type can be either REAL or INT, but only REAL is supported for now
        """
        self.write('WLIS:WAV:NEW "{}" {}'.format(name, size, type))

    @Action()
    def delete_waveform(self, name):
        """Delete wfm <name>.  If <name>=='ALL', deletes all user defined waveform"""
        if name == 'ALL': self.write('WLIS:WAV:DEL ALL')
        else: self.write('WLIS:WAV:DEL "{}"'.format(name))




if __name__=='__main__':
    awg = AWG5014C('TCPIP0::192.168.1.104::4444::SOCKET')
    awg.initialize()