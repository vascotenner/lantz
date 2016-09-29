# -*- coding: utf-8 -*-
"""
    lantz.drivers.newport.fsm300
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation of FSM300 using NI DAQ controller

    Author: Kevin Miao
    Date: 9/27/2016
"""

from lantz import Driver
from lantz.driver import Feat, DictFeat
from lantz.drivers.ni.daqmx import AnalogOutputTask, VoltageOutputChannel

from lantz import Q_

import time

import numpy as np

class FSM300(Driver):

    def __init__(self, x_ao_ch, y_ao_ch,
                 ao_smooth_rate=Q_('10 kHz'), ao_smooth_steps=Q_('1000 1/V'),
                 limits=((Q_(-10, 'V'), Q_(10, 'V')), (Q_(-10, 'V'), Q_(10, 'V'))),
                 cal=(Q_(9.5768, 'um/V'), Q_(7.1759, 'um/V'))):
        x_limits_mag = tuple(float(val / Q_('1 V')) for val in limits[0])
        y_limits_mag = tuple(float(val / Q_('1 V')) for val in limits[1])
        self.task = AnalogOutputTask('fsm300')
        VoltageOutputChannel(x_ao_ch, name='fsm_x', min_max=x_limits_mag, units='volts', task=self.task)
        VoltageOutputChannel(y_ao_ch, name='fsm_y', min_max=y_limits_mag, units='volts', task=self.task)
        self.ao_smooth_rate = ao_smooth_rate
        self.ao_smooth_steps = ao_smooth_steps
        self.cal = cal

        self._position = (Q_('0 um'), Q_('0 um'))

        super().__init__()

        return

    def ao_smooth_func(self, init_point, final_point):
        init_x, init_y = init_point
        final_x, final_y = final_point

        init_x_voltage, final_x_voltage = init_x / self.cal[0], final_x / self.cal[0]
        init_y_voltage, final_y_voltage = init_y / self.cal[1], final_y / self.cal[1]
        diff_x_voltage = final_x_voltage - init_x_voltage
        diff_y_voltage = final_y_voltage - init_y_voltage

        diff_voltage = max(abs(diff_x_voltage), abs(diff_y_voltage))
        steps = int(np.ceil(diff_voltage * self.ao_smooth_steps))
        init = np.array([val.to('V').magnitude for val in [init_x_voltage, init_y_voltage]])
        diff = np.array([val.to('V').magnitude for val in [diff_x_voltage, diff_y_voltage]])

        versine_steps = (1.0 - np.cos(np.linspace(0.0, np.pi, steps))) / 2.0

        step_voltages = np.outer(np.ones(steps), init) + np.outer(versine_steps, diff)
        return step_voltages

    @Feat()
    def abs_position(self):
        return self._position


    @abs_position.setter
    def abs_position(self, point):
        x, y = point
        if not isinstance(x, Q_):
            x = Q_(x, 'um')
        if not isinstance(y, Q_):
            y = Q_(y, 'um')
        point = x, y
        step_voltages = self.ao_smooth_func(self._position, point)
        if step_voltages.size:
            steps = step_voltages.shape[0]
            clock_config = {
                'source': 'OnboardClock',
                'rate': self.ao_smooth_rate.to('Hz').magnitude,
                'sample_mode': 'finite',
                'samples_per_channel': steps,
            }
            self.task.configure_timing_sample_clock(**clock_config)
            self.task.write(data=step_voltages, auto_start=False, timeout=0, group_by='scan')
            self.task.start()
            time.sleep((steps / self.ao_smooth_rate).to('s').magnitude)
            self.task.stop()
        self._position = point


    @Action()
    def line_scan(self, init_point, final_point, acq_task):
        step_voltages = self.ao_smooth_func(init_point, final_point)
        steps = step_voltages.shape[0]
        clock_config = {
            'source': 'OnboardClock',
            'rate': self.ao_smooth_rate.to('Hz').magnitude,
            'sample_mode': 'finite',
            'samples_per_channel': steps,
        }

        self.abs_position = init_point
        self.task.configure_timing_sample_clock(**clock_config)
        acq_task.configure_timing_sample_clock(**clock_config)
        self.task.configure_trigger_digital_edge_start('ai/StartTrigger')
        self.task.start()
        acq_task.start()
        scanned = acq_task.read(samples_per_channel=steps)
        acq_task.stop()
        self.task.stop()
        return scanned
