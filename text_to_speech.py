from gtts import gTTS
import os

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows, use "afplay output.mp3" for macOS, "mpg321 output.mp3" for Linux

# Example usage
text = "Hello, this is a test."
text_to_speech(text)