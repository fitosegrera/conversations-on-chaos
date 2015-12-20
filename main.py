#!/usr/bin/env python

import os
import serial
import time

ser = serial.Serial("/dev/ttyAMA0", 9600)
id1 = "1"
id2 = "2"
comInit = "%"
comEnd = "$"
cycleLimit = 30
rows, columns = os.popen('stty size', 'r').read().split()

def initCycle(id, t):
        global ser
        ser.write(comInit + id + ";")
        time.sleep(t)

def endCycle(id, t):
        global ser
        ser.write(comEnd + id + ";")
        time.sleep(t)
        print "ID:", id
        print ser.readline()

def printMsg(msg):
        line = ""
        for c in range((int(columns)*int(rows)) / 2):
        	line += " "
        print line
        half = int(columns)/2
        print "\n\n"
        halfLine = ""
        for i in range(half - int(len(msg))/2):
        	halfLine += " "
        print halfLine, msg
        print "\n\n"
        line = ""
        for c in range((int(columns)*int(rows)) / 2):
        	line += " "
        print line

def main():
		global cycleLimit
		printMsg("CHAOTIC CYCLE INITIATED...")
		initCycle("1", 3)
		initCycle("2", 3)
		time.sleep(cycleLimit)
		print "\n"
		printMsg("RECEIVING DATA FROM AGENTS...")
		endCycle("1", 10)
		endCycle("2", 10)
		time.sleep(3)

while True:
		try:
		        main()
		        time.sleep(10)

		except KeyboardInterrupt:
		        exit(0)
