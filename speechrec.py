import speech_recognition as sr
from gtts import gTTS
import os
import serial

ticker = 0
ser = serial.Serial('COM3', 9600)

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
        response[1] = "Unable to recognize speech"

    return response

keyWords = {"takeoff": "Taking off", 
"land": "Landing" ,
'sweep': "Sweeping area" ,
'RTB': "Returning to base",
'return to base': "Returning to base",
'confirm': "Roger, bravo",
'track': "Identifying",
'engage': "Engaging",
'target': 'Red, bravo',
'hold': 'Holding, bravo',
'shift': 'Shifting target, bravo',
'weapons free': 'Weapons down, bravo',
'monitor': 'Monitoring, bravo',
'granted': 'Granted',
'detected': 'Detecting',
'reset1': 'Resetting pitch',
'reset2': 'Resetting yaw'}

def action(command):

    if command == 'takeoff':
        return 1
    elif command == 'land':
        return 2
    elif command == 'sweep':
        return 3
    elif command == 'RTB' or command == 'return to base':
        return 4
    elif command == 'confirm':
        return 5
    elif command == 'track':
        return 6
    elif command == 'engage':
        return 7
    elif command == 'target':
        return  8
    elif command == 'hold':
        return  9
    elif command == 'shift':
        return 10
    elif command == 'weapons free':
        return 11
    elif command == 'monitor':
        return 12
    elif command == 'granted':
        return 13
    elif command == 'detected':
        return 14
    elif command == 'reset1':
        return 15
    elif command == 'reset2':
        return 16
    return 0

def command_validation(response, dict):
    if response == 'none':
        return ("Command not detected")
    words = response.split()
    for word in words:
        if word in dict:
            return (dict[word])
            break
    return ("Command not found")

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
        newcmd = (recognizing_speech(r, m, command))[2]
        print(newcmd)
        keyword = command_validation(newcmd, keyWords)
        text_to_speech(keyword, my_validations_header)
        ticker = action(keyword)

        command = input('Enter y to input command, n to quit: ')
    elif command == 'n':
        print("Program Exited")
        break
    else:
        command = input('Command not valid, enter again (y/n): ')
        pass


