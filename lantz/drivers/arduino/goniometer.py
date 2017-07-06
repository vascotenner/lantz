# -*- coding: utf-8 -*-
"""
	lantz.drivers.arduino.goniometer
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	Lantz interface to the arduino controlling the goniometer

	Authors: Alexandre Bourassa
	Date: 3/28/2017

"""

from lantz import Action, Feat, DictFeat
from lantz.messagebased import MessageBasedDriver

from pyvisa.constants import Parity, StopBits

import time

class Goniometer(MessageBasedDriver):

	comm_delay = 1

	DEFAULTS = {
		'ASRL': {
			'write_termination': '\n',
			'read_termination': '\r\n',
			'baud_rate': 9600,
			'timeout': 2000,
		}
	}

	errors = {
	 -1:  'theta or phi were out of bounds',
	 -2:  'alpha or beta were out of bounds',
	 -3:  'attempted rotateTo while run_state != 0',
	 -4:  'period is out of bound',
	 -9:  'R is out of bounds',
	-10:  'Unknown cmd',
	-11:  'other error',
	-50:  'no error',
	}

		
	def initialize(self):
		super().initialize()
		time.sleep(2)
		self.query('stop')
		time.sleep(2)
	
	def check_error(self, err):
		if err != -50:
			raise Exception(self.errors[err])
		else:
			print("Success")
	
	def query(self, cmd):
		self.write(cmd)
		ans = self.read()
		err = int(self.read())
		self.check_error(err)
		return ans
	
	@Feat(limits=(70, 110, 0.01))
	def theta(self):
		return float(self.query('theta?'))

	@theta.setter
	def theta(self, val):
		float(self.query('theta {}'.format(val)))

	@Feat(limits=(30, 135, 0.01))
	def phi(self):
		return float(self.query('phi?'))

	@phi.setter
	def phi(self, val):
		return float(self.query('phi {}'.format(val)))
		
	@Feat() # units = mm
	def R(self):
		return float(self.query('getr'))
	
	@R.setter
	def R(self, val):
		return self.query('abs {}'.format(val))
	
	@Feat()
	def state(self):
		return self.query('state?')
		
	@Feat()
	def stop(self):
		self.query('stop')
		
	@Feat()
	def period(self):
		return self.query('period?')
	
	@period.setter
	def period(self, val):
		return self.query('pperiod {}'.format(val))

