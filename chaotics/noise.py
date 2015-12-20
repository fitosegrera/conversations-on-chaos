#!/usr/bin/env python

import random
from subprocess import Popen, PIPE

class Noise:

	def sinewave(self, period, freq):
		command =[ 
				'play', 
				'-n',
				'synth', 
				str(period), 
				'sin', 
				str(freq)
		]

		Popen(command, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)		

	def whitenoise(self, period, freq):
		command =[
                'play',
                '-n',
                'synth',
                str(period),
                'whitenoise',
                str(freq)
		]

		Popen(command, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)

	def generate(self, r):
		self.whitenoise(0.1, 50000)
		self.sinewave(10, 15000)
		for i in range(r):
			t1 = random.random() * (0.01 - 0.001) + 0.001
			t2 = random.random() * (0.01 - 0.0001) + 0.0001
			chance = random.randint(0, 100)
			self.sinewave(t1, 8000)
			self.sinewave(t2, 5000)
