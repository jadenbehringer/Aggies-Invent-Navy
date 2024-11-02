from gtts import gTTS
import os

my_validations_header = ['alpha', 'bravo', 'charlie', 'delta']

def text_to_speech(text, header, lang='en'):
    words = text.split()
    for word in words:
        if word in header:
            my_header = word
    text = ' '.join([word for word in words if word not in header])
    text = text + ' ' + my_header
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows, use "afplay output.mp3" for macOS, "mpg321 output.mp3" for Linux

# Example usage
text = "Hello, this is a bravo test."
text_to_speech(text, my_validations_header)