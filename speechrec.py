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

keyWords = {"Takeoff": "Taking off", 
"Land": "Landing" ,
'Sweep': "Sweeping area" ,
'Take': "Taking target" ,
'RTB': "Returning to base",
'Return to base': "Returning to base",
'Confirm': "Roger, bravo",
'Track': "Identifying",
'Engage': "Engaging",
'Target': 'Red, bravo',
'Hold': 'Holding, bravo',
'Shift': 'Shifting target, bravo',
'Weapons free': 'Weapons down, bravo',
'Monitor': 'Monitoring, bravo'}

def command_validation(response, dict):
    if response == 'None':
        return (0,"Command not detected")
    for x in response:
        if x in dict:
            return (1, dict[x])
            break
    return (0, "Command not found")


r = sr.Recognizer()
m = sr.Microphone()
command = input('Enter y to input command, n to quit: ')


while True:
    if command == 'y':
        mytup = command_validation((recognizing_speech(r, m, command))[2], keyWords)
        print(mytup(1))
        command = input('Enter y to input command, n to quit: ')
    elif command == 'n':
        print("Program Exited")
        break
    else:
        command = input('Command not valid, enter again (y/n): ')
        pass

    
