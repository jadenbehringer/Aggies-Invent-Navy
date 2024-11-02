#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 12:25:44 2024

@author: sb
"""

import pyttsx3
import random
from time import sleep
def response_bot(text):
    
    my_validations_header = ['Alpha', 'Bravo', 'Charlie', 'Delta']

    my_validations_header_prompt = my_validations_header[random.randint(0,3)]


    my_int = random.randint(1,12)

    engine = pyttsx3.init()

    """ RATE"""

    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 180)
    
    if 'kill' in text.lower():
        engine.say('Killing program.')
        engine.runAndWait()
        return True
    else:
        engine.say('No clear order given.')
        engine.runAndWait()
        return False




'''my_validations_header = ['Alpha', 'Bravo', 'Charlie', 'Delta']

my_validations_header_prompt = my_validations_header[random.randint(0,3)]


my_int = random.randint(1,12)

engine = pyttsx3.init()

""" RATE"""

rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 180)'''


response_bot('Kill!')
sleep(4)
response_bot('No the event')




