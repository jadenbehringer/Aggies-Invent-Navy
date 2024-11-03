import speech_recognition as sr
from gtts import gTTS
import os
import serial
import time

ticker = 0

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

def text_to_speech(text, header, lang='en'):
    words = text.split()
    my_header =''
    for word in words:
        if word.lower() in header:
            my_header = word
    text = ' '.join([word for word in words if word not in header])
    text = text + ' ' + my_header
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows, use "afplay output.mp3" for macOS, "mpg321 output.mp3" for Linux

keyWords = {
"take": "Taking off", 
"off": "Taking off",
"takeoff": "Taking off",
"land": "Landing" ,
"landing": "Landing",
'sweep': "Sweeping area" ,
'scout': "Sweeping area",
'RTB': "Returning to base",
'return': "Returning to base",
'base': "Returning to base",
'fire': "Confiming target",
'engage': "Confirming target"
}

confirmWords = ['confirm', 'granted', 'yes' , 'roger', 'affirmative', 'positive']

def get_val(command):
    if command == "Taking off":
        return 1
    elif command == 'Landing':
        return 2
    elif command == 'Sweeping area':
        return 3
    elif command == 'Returning to base':
        return 4
    elif command == 'Confirming target':
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
        if word in dict:
            return (dict[word])
            break
    return ("Unkown command")

def permission_validation(response, confirmedWords):
    if response == 'none':
        return ("Unable to recognize speech, please restate command")
    words = response.split()
    for word in words:
        if word in confirmedWords:
            return ("Roger, engaging")
    return ("Permission not detected, will not engage")


def requesting_permission(r, m, confirmWords, valheader):
    speech = recognizing_speech(r, m)[2]
    response = permission_validation(speech, confirmWords)
    text_to_speech(response, valheader)
    return [speech, response]

r = sr.Recognizer()
m = sr.Microphone()
cntrl = input('Enter y to input command, n to quit: ')

my_validations_header = ['alpha', 'bravo', 'charlie', 'delta']


while True:
    if cntrl == 'y':
        ticker = 0
        speech = (recognizing_speech(r, m))[2]
        print(speech)
        response = command_validation(speech, keyWords)
        text_to_speech(response, my_validations_header)
        ticker = get_val(response)
        if action(ticker) == 1:
            time.sleep(3.5)
            text_to_speech('Target spotted, requesting permission to engage', my_validations_header)
            time.sleep(4)
            permission = 'none'
            while permission == 'none':
                list1 = requesting_permission(r, m, confirmWords, my_validations_header)
                permission = list1[0]
                response = list1[1]
                text_to_speech(response, my_validations_header)
                time.sleep(3.5)
            if response == 'Roger, engaging':
                action(5)
                time.sleep(2)
                text_to_speech('Target Destroyed, awaiting next command', my_validations_header)
        elif action(ticker) == 2:
            time.sleep(3.5)
            text_to_speech('Requesting confirmation to engage', my_validations_header)
            time.sleep(4)
            permission = 'none'
            while permission == 'none':
                list1 = requesting_permission(r, m, confirmWords, my_validations_header)
                permission = list1[0]
                response = list1[1]
                text_to_speech(response, my_validations_header)
                time.sleep(3.5)
            if response == 'Roger, engaging':
                action(5)
                time.sleep(2)
                text_to_speech('Target Destroyed, awaiting next command', my_validations_header)
        ticker = 0
        cntrl = input('Enter y to input command, n to quit: ')
    elif cntrl == 'n':
        ticker = 0
        print("Program Exited")
        break
    else:
        cntrl = input('Cntrl not valid, enter again (y/n): ')
        pass


