import speech_recognition as sr


def recognizing_speech(recognizer, microphone, command):
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
'take': "Taking target" ,
'RTB': "Returning to base",
'return to base': "Returning to base",
'confirm': "Roger, bravo",
'track': "Identifying",
'engage': "Engaging",
'target': 'Red, bravo',
'hold': 'Holding, bravo',
'shift': 'Shifting target, bravo',
'weapons free': 'Weapons down, bravo',
'monitor': 'Monitoring, bravo'}

def command_validation(response, dict):
    if response == 'none':
        return ("Command not detected")
    words = response.split()
    for word in words:
        if word in dict:
            return (dict[word])
            break
    return ("Command not found")


r = sr.Recognizer()
m = sr.Microphone()
command = input('Enter y to input command, n to quit: ')


while True:
    if command == 'y':
        newcmd = (recognizing_speech(r, m, command))[2]
        print(newcmd)
        valid = command_validation(newcmd, keyWords)
        print(valid)
        command = input('Enter y to input command, n to quit: ')
    elif command == 'n':
        print("Program Exited")
        break
    else:
        command = input('Command not valid, enter again (y/n): ')
        pass


