import speech_recognition as sr
from gtts import gTTS
import os
import serial
import time

ticker = 0



#python C:\Users\medve\Downloads\serialtest.py

# Configure the serial port
ser = serial.Serial('COM3', 9600)  # Replace 'COM1' with your serial port
ser.close()
ser.open()

def write_to_serial(command):
    # Output the string "tko\n"
    utf = command.encode('utf-8')
    ser.write(utf)
    # Close the serial port

def recognizing_speech(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    
    response = [True, "none", "none"]
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try: 
        response[2] = recognizer.recognize_google(audio)

    except sr.RequestError:
        response[0] = False
        response[1] = "API unavailable"

    except sr.UnknownValueError:
        response[1] = "Unable to recognize speech, please restate command"

    return response

def tts(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("start output.mp3")  


keyWords = {
"take": "Rodger, Lima one-six-two, Taking off", 
"off": "Rodger, Lima one-six-two, Taking off",
"takeoff": "Rodger, Lima one-six-two, Taking off",
"land": "Rodger, Lima one-six-two, Landing" ,
"landing": "Rodger, Lima one-six-two, Landing",
'sweep': "Rodger, Lima one-six-two, searching sector alpha" ,
'reconnaissance': "Rodger, Lima one-six-two, searching sector alpha" ,
'search' : 'Rodger, Lima one-six-two, searching sector alpha',
'sector' : 'Rodger, Lima one-six-two, searching sector alpha',
'scout': "Rodger, Lima one-six-two, Sweeping area",
'RTB': "Rodger, Lima one-six-two, Returning to base",
'return': "Rodger, Lima one-six-two, Returning to base",
'base': "Rodger, Lima one-six-two, Returning to base",
'fire': "Rodger, Lima one-six-two, target confirmed",
'engage': "Rodger, Lima one-six-two, target confirmed",
'engagement': "Rodger, Lima one-six-two, target confirmed"
}


confirmWords = ['confirm','confirmed', 'granted', 'yes' , 'roger', 'affirmative', 'positive', 'approved', 'fire']

def get_val(command):
    if command == "Rodger, Lima one-six-two, Taking off":
        return 1
    elif command == 'Rodger, Lima one-six-two, Landing':
        return 2
    elif command == 'Rodger, Lima one-six-two, searching sector alpha':
        return 3
    elif command == 'Rodger, Lima one-six-two, Returning to base':
        return 4
    elif command == 'Rodger, Lima one-six-two, target confirmed':
        return 6
    
def action(val):
    if val == 1:
        write_to_serial('tko\n')
        return 0
    elif val == 2:
        write_to_serial('lng\n')
        return 0
    elif val == 3:
        write_to_serial('pt1\n')
        return 1
    elif val == 4:
        write_to_serial('rya\n')
        return 0
    elif val == 5:
        write_to_serial('pt2\n')
    elif val == 6:
        return 2

def test_action(val):
    if val == 1:
        #write_to_serial('tko\n')
        return 0
    elif val == 2:
        #write_to_serial('lng\n')
        return 0
    elif val == 3:
        #write_to_serial('pt1\n')
        return 1
    elif val == 4:
        #write_to_serial('rya\n')
        return 0
    elif val == 5:
       #write_to_serial('pt2\n')
       pass
    elif val == 6:
        return 2

def command_validation(response, dict):
    if response == 'none':
        return ("Unable to recognize speech")
    words = response.split()
    for word in words:
        if word.lower() in dict:
            return (dict[word.lower()])
            break
    return ("Unknown command")

def permission_validation(response, confirmedWords):
    if response == 'none':
        return ("Unable to recognize speech, please restate command")
    words = response.split()
    for word in words:
        if word in confirmedWords:
            return ("Rodger, Lima one-six-two, engaging")
    return ("Lima one-six-two Permission denied, will not engage")


def requesting_permission(r, m, confirmWords):
    speech = recognizing_speech(r, m)[2]
    response = permission_validation(speech, confirmWords)
    tts(response)
    return [speech, response]

r = sr.Recognizer()
m = sr.Microphone()
cntrl = input('Enter y to input command, n to quit: ')

my_validations_header = ['alpha', 'bravo', 'charlie', 'delta', 'lima']


while True:
    if cntrl == 'y':
        ticker = 0
        speech = (recognizing_speech(r, m))[2]
        print(speech)
        response = command_validation(speech, keyWords)
        tts(response)
        ticker = get_val(response)
        mynum = action(ticker)
        if mynum == 1:
            time.sleep(4)
            tts('bogey spotted, requesting permission to engage')
            time.sleep(4)
            permission = 'none'
            while permission == 'none':
                list1 = requesting_permission(r, m, confirmWords)
                permission = list1[0]
                response = list1[1]
                tts(response)
                time.sleep(3.5)
            if response == 'Rodger, Lima one-six-two, engaging':
                action(5)
                time.sleep(2)
                tts('Lima one-six-two... Target Destroyed, awaiting next command')
        elif mynum == 2:
            time.sleep(4)
            tts('Requesting confirmation to engage')
            time.sleep(4)
            permission = 'none'
            while permission == 'none':
                list1 = requesting_permission(r, m, confirmWords)
                permission = list1[0]
                response = list1[1]
                tts(response)
                time.sleep(3.5)
            if response == 'Rodger, Lima one-six-two, engaging':
                action(5)
                time.sleep(2)
                tts('Lima one-six-two... Target Destroyed, awaiting next command')
        ticker = 0
        cntrl = input('Enter y to input command, n to quit: ')
    elif cntrl == 'n':
        ticker = 0
        print("Program Exited")
        break
    else:
        cntrl = input('Cntrl not valid, enter again (y/n): ')
        pass
