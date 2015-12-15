# Demo code to control Newport FSM, based off of original by David J. Christle
# Original code here:
# https://github.com/dchristle/qtlab/blob/master/instrument_plugins/Newport_FSM.py

from lantz.drivers.ni.daqmx import System
from lantz.drivers.ni.daqmx import AnalogOutputTask, VoltageOutputChannel

from lantz import Feat, DictFeat, Action

from numpy import abs, ceil, pi, linspace, cos, ones


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

            chan = VoltageOutputChannel(phys_chan, name=chan_name,
                                        min_max=(V_min, V_max), units='volts',
                                        task=self.task)
        self.task.start()

        from numpy.random import randn

        data = randn(1000, 1000)

        self.task.write(data, auto_start=False, timeout=10.0, group_by='scan')

        print('Task started!')

    def finalize(self):
        """
        Stops AO tasks for controlling FSM.
        """
        self.task.stop()

    @Feat()
    def abs_position_pair(self):
        x_loc = abs_position_single['x']
        y_loc = abs_position_single['y']
        print('FSM at ({}um,{}um)'.format(x_loc, y_loc))
        return [x_loc, y_loc]

    @abs_position_pair.setter
    def abs_position_pair(self, xy_pos):
        """
        Sets absolute position of scanning mirror, as a micron pair.
        """
        abs_position_single['x'] = xy_pos[0]
        abs_position_single['y'] = xy_pos[1]
        print('Set FSM to ({}um,{}um).'.format(xy_pos[0], xy_pos[1]))
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

    # @Feat()
    # def scan_speed(self):
    #     """
    #     Returns current FSM scan speed in V/s.
    #     """
    #     print('Bold faced lie')
    #     return 0
    #
    # @scan_speed.setter
    # def scan_speed(self, speed):
    #     """
    #     Sets the current scan speed of the analog output in V/s.
    #     """
    #     print('Bold faced lie')
    #     return 0

    def convert_V_to_um(self, dime, V):
        """
        Returns micron position corresponding to channel voltage.
        """
        um = V * self.fsm_dimensions[dim]['micron_per_volt'] + (
            self.fsm_dimensions[dim]['origin'])
        return um

    def convert_um_to_V(self, dim, um):
        """
        Returns voltage corresponding to micron position.
        """
        V = (um - self.fsm_dimensions[dim]['origin']) / (
            self.fsm_dimensions[dim]['micron_per_volt'])
        return V

    def set_V_to_zero(self):
        """
        Sets output voltages to 0.
        """

    @Action()
    def ao_smooth(self, x_init, x_final, channel):
        """
        Smooths output of DAQ to avoid hysteresis w/ moving FSM mirror.

        Copy of dchristle's algorithm. (I know what you're trying to do, and
        just stop.)
        """
        ao_smooth_rate = 50000.0  # Hz
        ao_smooth_steps_per_volt = 1000.0  # steps/V

        v_init = self.convert_um_to_V(x_init, channel)
        v_final = self.convert_un_to_V(x_final, channel)

        n_steps = ceil(abs(v_final - v_init) * ao_smooth_steps_per_volt)

        v_data = v_init * ones(n_steps) + (v_final - v_init) * (1.0 - cos(
            linspace(0, pi, n_steps) / 2.0))

        print(v_data)

if __name__ == '__main__':
    with Newport_FSM() as inst:
        print('testing!')
