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

confirmWords = ['confirm', 'granted', 'yes' , 'roger', 'affirmative']

def get_val(command):
    if command == "Taking off":
        return 1
    elif command == 'Landing':
        return 2
    elif command == 'Sweeping area':
        return 3
    elif command == 'Returning to base':
        return 4
    elif command == 'Confiming target':
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


def command_validation(response, dict):
    if response == 'none':
        return ("Command not detected")
    words = response.split()
    for word in words:
        if word in dict:
            return (dict[word])
            break
    return ("Command not found")

def requesting_permission(response):

def permission_validation(response, confirmedWords):
    if response == 'none':
        return ("Permission not detected, will not engage")
    words = response.split()
    for word in words:
        if word in confirmedWords:
            return ("Roger, engaging")
    return ("Unable to recognize speech, please restate command")

def text_to_speech(text, header, lang='en'):
    words = text.split()
    my_header =''
    for word in words:
        if word in header:
            my_header = word
    text = ' '.join([word for word in words if word not in header])
    text = text + ' ' + my_header
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows, use "afplay output.mp3" for macOS, "mpg321 output.mp3" for Linux


r = sr.Recognizer()
m = sr.Microphone()
command = input('Enter y to input command, n to quit: ')

my_validations_header = ['alpha', 'bravo', 'charlie', 'delta']


while True:
    if command == 'y':
        newcmd = (recognizing_speech(r, m))[2]
        print(newcmd)
        keyword = command_validation(newcmd, keyWords)
        text_to_speech(keyword, my_validations_header)
        ticker = get_val(keyword)
        if action(ticker) == 1:
            time.sleep(2)
            text_to_speech('Target spotted, permission to engage', my_validations_header)
            confirmcommand = 'none'
            while confirmcommand == 'none':
                time.sleep(2)
                confirmcommand = recognizing_speech(r, m)[2]
                response2 = (permission_validation(confirmcommand, confirmWords))
                text_to_speech(response2, my_validations_header)
            if response2 == 'Roger, engaging':
                action(5)
                time.sleep(1)
                text_to_speech('Target Destroyed', my_validations_header)
        ticker = 0
        command = input('Enter y to input command, n to quit: ')
    elif command == 'n':
        print("Program Exited")
        break
    else:
        command = input('Command not valid, enter again (y/n): ')
        pass


