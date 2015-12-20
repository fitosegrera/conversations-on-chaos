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
cycleLimit = 30
(rows, columns) = os.popen('stty size', 'r').read().split()

audio = noise.Noise()
voice = conversation.Conversation()


def run():
    file = open("input.txt", 'r')
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

    audio.alert(12, 0.2, 900)
    random_index = random.randint(0, len(words))
    tmp_sentence = ''
    tosay = ''
    poschecker = 0

    while True:
        if dict.has_key(key):
            word = random.choice(dict[key])  # this is where the randomness takes place
            tmp_sentence += str(word + ' ')
            print word,
            key = (key[1], word)
            if key in end_sentence:
                rand = random.random() * (0.01 - 0.001) + 0.001
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

    print ''
    print tosay
    with open('output.txt', 'w') as text_file:
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
        text_file.write(towrite)
    points = ""
    for c in range(int(columns)):
        points += "."
    for i in range(10):
        print points
        audio.generate(5, 2)
        time.sleep(0.01)
    printMsg('SPEAKING...')
    time.sleep(4)
    voice.say(tmp_sentence)
    printMsg(towrite)
    time.sleep(4)

def initCycle(id, t):
    ser.write(comInit + id + ';')
    time.sleep(t)


def endCycle(id, t):
    global ser
    ser.write(comEnd + id + ';')
    time.sleep(t)
    print 'ID:', id
    print ser.readline()


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
    global cycleLimit
    printMsg('CHAOTIC CYCLE INITIATED...')
    initCycle('1', 3)
    initCycle('2', 3)
    time.sleep(cycleLimit)
    print '\n'
    printMsg('RECEIVING DATA FROM AGENTS...')
    endCycle('1', 10)
    endCycle('2', 10)
    time.sleep(3)


while True:
    try:
        main()
        time.sleep(10)
        run()
        time.sleep(15)
        run()
        time.sleep(15)

    except KeyboardInterrupt:

        exit(0)



