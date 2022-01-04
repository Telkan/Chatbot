from os import remove

import vlc

import speech_recognition as sr  
from gtts import gTTS
import time
from io import BytesIO

def textToSpeech(outputText):
    audioFilePointer = BytesIO()
    tts = gTTS(outputText)
    tts.write_to_fp(audioFilePointer)
    

    pass 

p = vlc.MediaPlayer('temp.mp3')
p.play()
#get audio from the microphone                                                                       
r = sr.Recognizer()                                                                                   

with sr.Microphone() as source:                                                                       
    print("Speak:")                                                                                   
    audio = r.listen(source,10,4)       
    
try:
    print("You said " + r.recognize_google(audio))
    print("asdfasdfasdf not ")
    tts = gTTS(r.recognize_google(audio))
    os:remove('temp.mp3')
    tts.save('temp.mp3')
    print("asdfasdfasdf not ")
    p = vlc.MediaPlayer('temp.mp3')
    p.play()
    
    print("asdfasdfasdf not ")
    
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))


