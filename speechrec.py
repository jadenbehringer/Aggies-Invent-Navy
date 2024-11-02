import speech_recognition as sr


def recognizing_speech(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    
    response = {
    "success": True,
    "error": None,
    "transcription": None
    }

    command = input('Enter y for command, n to quit: ')

    while True:
        if command == 'y':
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
        elif command == 'n':
            return "Program Exited"
        else:
            command = input('Command not valid, enter again (y/n): ')
            pass

r = sr.Recognizer()
m = sr.Microphone()

print (recognizing_speech(r, m))


