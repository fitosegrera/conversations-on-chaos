#!/usr/bin/env python

#Class to use the espeak TTS engine with python
#Author: fito_segrera / http://fii.to

from subprocess import Popen, PIPE
class Conversation:

	def say(self, tosay):
		#os.system("espeak " + "\"" + tosay + "\"")
		command =[ 
				'espeak', 
				"-f",
				"output.txt" 
		]

		Popen(command, stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)