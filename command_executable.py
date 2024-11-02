#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 16:30:55 2024

@author: sb
"""

import pyttsx3
import random
from time import sleep
import speech_recognition as sr

def bot_response(filename):
    
    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)

    print(text)
    
    my_validations_header = ['alpha', 'bravo', 'charlie', 'delta']
    text = text.lower()
    my_text = text.split(' ')
    
    for element in my_text:
        if element in my_validations_header:
            val_header = str(element)
            break
        else:
            val_header = ' '
    
    #Define the responses
    
    keyWords = {
"takeoff": "Taking off", 
"land": "Landing" ,
'sweep': "Sweeping area" ,
'take': "Taking target" ,
'rtb': "Returning to base",
'return': "Returning to base",
'confirm': "Roger",
'track': "Identifying",
'engage': "Engaging",
'target': 'Red',
'hold': 'Holding',
'shift': 'Shifting target',
'weapons': 'Weapons down',
'monitor': 'Monitoring'
}
        
    engine = pyttsx3.init()
    
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 180)
    
    executable = text[0:(text.find(' '))].strip()
    #print(val_header)
    
    return_statement = str(str(keyWords.get(executable)) + str(val_header))
        
    engine.say(return_statement)
    engine.runAndWait()
    return val_header
    
bot_response('/Users/sb/Downloads/WP_free.wav')
# sleep(0.1)