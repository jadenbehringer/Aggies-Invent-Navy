import speech_recognition as sr


def recognizing_speech(recognizer, microphone, command):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    
    response = {
    "success": True,
    "error": None,
    "transcription": None
    }
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try: 
        response["transcription"] = recognizer.recognize_google(audio)

    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"

    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response


r = sr.Recognizer()
m = sr.Microphone()
command = input('Enter y to input command, n to quit: ')

while True:
    if command == 'y':
        print (recognizing_speech(r, m, command))
        command = input('Enter y to input command, n to quit: ')
    elif command == 'n':
        print("Program Exited")
        break
    else:
        command = input('Command not valid, enter again (y/n): ')
        pass

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
    if response[2] == 'None':
        return (0,"Command not detected")
    for x in response[2]:
        if x in dict:
            return (1, dict[x])
            break
    return (0, "Command not found")

