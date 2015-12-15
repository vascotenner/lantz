# Demo code to control Newport FSM, based off of original by David J. Christle
# Original code here: https://github.com/dchristle/qtlab/blob/master/instrument_plugins/Newport_FSM.py
from lantz.drivers.ni.daqmx import System, AnalogOutputTask, VoltageOutputChannel

from lantz import Feat, DictFeat, Action

class Newport_FSM(System):
    """
    Class for controlling Newport FSM using National Instruments DAQ.
    """



    def initialize(self):
        """
        Creates AO tasks for controlling FSM.
        """
        self.task = AnalogOutputTask('FSM')

        self.dev_name = 'dev1/'

        self.fsm_dimensions = {
            'x': {'micron_per_volt': 9.5768,
                  'min_v': -10.0,
                  'max_v': +10.0,
                  'default': 0.0,
                  'origin': 0.0,
                  'ao_channel': 'ao0'},
            'y': {'micron_per_volt': 7.1759,
                  'min_v': -10.0,
                  'max_v': +10.0,
                  'default': 0.0,
                  'origin': 0.0,
                  'ao_channel': 'ao1'}
        }

        for dim in self.fsm_dimensions:
            chan_name = dim
            phys_chan = self.dev_name + self.fsm_dimensions[dim]['ao_channel']
            V_min = self.fsm_dimensions[dim]['min_v']
            V_max = self.fsm_dimensions[dim]['max_v']
            print(phys_chan)

            print('Creating voltage output channel')
            print(V_min)
            print(V_max)

            chan = VoltageOutputChannel(phys_chan, name=chan_name,
                                        min_max=(V_min, V_max), units='volts',
                                        task=self.task)
        self.task.start()
        print('Started task!')

    def finalize(self):
        """
        Stops AO tasks for controlling FSM.
        """


    @Feat()
    def abs_position_pair(self):
        """
        Absolute position of scanning
        """
        return 0

    @abs_position_pair.setter
    def abs_position_pair(self, xy_pos):
        """
        Sets absolute position of scanning mirror, as a micron pair.
        """
        return 0

    @DictFeat()
    def abs_position_single(self, dimension):
        """
        Returns absolute position of scanning mirror along dimension.
        """
        return 0

    @abs_position_single.setter
    def abs_position_single(self, dimension, pos):
        """
        Sets absolute position of scanning mirror along dimension to be pos.
        """
        return 0


    @Feat()
    def scan_speed(self):
        """
        Returns current FSM scan speed in V/s.
        """
        return 0

    @scan_speed.setter
    def scan_speed(self, speed):
        """
        Sets the current scan speed of the analog output in V/s.
        """
        return 0

    def convert_V_to_um(self, dimension, V):
        """
        Returns micron position corresponding to channel voltage.
        """
        return 0

    def convert_um_to_V(self, dimension, um):
        """
        Returns voltage corresponding to micron position.
        """
        return 0

    def set_V_to_zero(self):
        """
        Sets output voltages to 0.
        """


if __name__ == '__main__':
    with Newport_FSM() as inst:
        print('testing!')
