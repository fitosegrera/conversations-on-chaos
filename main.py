#!/usr/bin/python

from chaotics import conversation
from chaotics import noise
import os
import serial
import time
import string
import random

ser = serial.Serial('/dev/ttyAMA0', 9600)
id1 = '1'
id2 = '2'
comInit = '%'
comEnd = '$'
inDataA = ""
inDataB = ""
cycleLimit = 30
(rows, columns) = os.popen('stty size', 'r').read().split()

audio = noise.Noise()
voice = conversation.Conversation()


def run(agentName, useSound):
    file = open("texts/input.txt", 'r')
    text = file.read()
    file.close()
    words = string.split(text)

    end_sentence = []
    dict = {}
    prev1 = ''
    prev2 = ''
    for word in words:
        if prev1 != '' and prev2 != '':
            key = (prev2, prev1)
            if dict.has_key(key):
                dict[key].append(word)
            else:
                dict[key] = [word]
                if prev1[-1:] == '.':
                    end_sentence.append(key)
        prev2 = prev1
        prev1 = word

    if end_sentence == []:
        print 'Sorry, there are no sentences in the text.'
        return

    key = ()
    count = len(words) / 10

    if useSound:
        audio.alert(12, 0.2, 900)
    random_index = random.randint(0, len(words))
    tmp_sentence = ''
    tosay = ''
    poschecker = 0

    while True:
        if dict.has_key(key):
            word = random.choice(dict[key])  # this is where the randomness takes place
            tmp_sentence += str(word + ' ')
            if useSound:
                print word,
            key = (key[1], word)
            if key in end_sentence:
                rand = random.random() * (0.01 - 0.001) + 0.001
                if useSound:
                        audio.whitenoise(rand, random.randint(10, 50))
                        time.sleep(0.05)
                        print
                count = count - 1
                if count <= 0:
                    break
        else:
            key = random.choice(end_sentence)
        if poschecker == random_index:
            tosay = tmp_sentence
        poschecker += 1

    if useSound:
        print ''
        print tosay

    with open('texts/output.txt', 'a') as text_file:
        short = string.split(tosay)
        towrite = ''
        rang = None
        if len(short) > 30:
            rang = 30
        else:
            rang = len(short)
        for w in range(rang):
            towrite += short[w] + ' '
            if (short[w])[-1:] == '.':
                break
        text_file.write(agentName + ": " + towrite + "\n\n")
    points = ""
    for c in range(int(columns)):
        points += "."

    if useSound:
        for i in range(10):
            print points
            audio.generate(5, 2)
            time.sleep(0.01)

    printMsg('SPEAKING...')
    time.sleep(4)
    # voice.say(tmp_sentence)
    voice.writeWav(towrite, agentName)
    printMsg(agentName + ": " + towrite)
    voice.playWav(agentName)
    time.sleep(4)

def initCycle(id, t):
    ser.write(comInit + id + ';')
    time.sleep(t)


def endCycle(id, t):
    global ser
    ser.write(comEnd + id + ';')
    time.sleep(t)
    inDat = ser.readline()
    print 'ID:', id
    print inDat
    return inDat

def processData(dataToProcess):
    splitted = dataToProcess.split()
    for d in splitted:
        print d

def printMsg(msg):
    line = ''
    for c in range(int(columns) * int(rows) / 2):
        line += ' '
    print line
    half = int(columns) / 2
    print 
    halfLine = ''
    for i in range(half - int(len(msg)) / 2):
        halfLine += ' '
    print halfLine, msg
    print 
    line = ''
    for c in range(int(columns) * int(rows) / 2):
        line += ' '
    print line


def main():
    global cycleLimit, inDataA, inDAtaB
    inDataA = ""
    inDataB = ""
    printMsg('CHAOTIC CYCLE INITIATED...')
    initCycle('1', 3)
    initCycle('2', 3)
    time.sleep(cycleLimit)
    print '\n'
    printMsg('RECEIVING DATA FROM AGENTS...')
    inDataA = endCycle('1', 10)
    processData(inDataA)
    inDataB = endCycle('2', 10)
    processData(inDAtaB)
    time.sleep(3)


while True:
    try:
        main()
        time.sleep(10)
        run("A", True)
        time.sleep(8)
        run("B", False)
        time.sleep(8)

    except KeyboardInterrupt:

        exit(0)



