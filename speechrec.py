import speech_recognition as sr
from gtts import gTTS
import os
import serial

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
        response[1] = "Unable to recognize speech"

    return response

keyWords = {"take": "Taking off", 
"land": "Landing" ,
'sweep': "Sweeping area" ,
'RTB': "Returning to base",
'return': "Returning to base",
'confirm': "Roger",
'engage': "Engaging",
'granted': 'Roger',
'denied': 'Denied'}

def get_val(command):

    if command == "Taking off":
        return 1
    elif command == 'Landing':
        return 2
    elif command == 'Sweeping area':
        return 3
    elif command == 'Returning to base':
        return 4
    elif command == 'Roger':
        return 5
    elif command == 'Engaging':
        return 6
    elif command == 'Denied':
        return 7
    
def action(val):
    if val == 1:
        write_to_serial('tko\n')
    elif val == 2:
        write_to_serial('lng\n')
    elif val == 3:
        write_to_serial('pt1\n')
    elif val == 4:
        write_to_serial('rya\n')
    elif val == 5:
        write_to_serial('pt2\n')

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
        newcmd = (recognizing_speech(r, m))[2]
        print(newcmd)
        keyword = command_validation(newcmd, keyWords)
        text_to_speech(keyword, my_validations_header)
        ticker = get_val(keyword)
        action(ticker)
        ticker = 0
        command = input('Enter y to input command, n to quit: ')
    elif command == 'n':
        print("Program Exited")
        break
    else:
        command = input('Command not valid, enter again (y/n): ')
        pass


