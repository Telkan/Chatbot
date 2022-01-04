from os import remove
import winsound
import vlc
import socket
import speech_recognition as sr  
from gtts import gTTS
from playsound import playsound
import time
from io import BytesIO

def textToSpeech(outputText):
    audioFilePointer = BytesIO()
    tts = gTTS(outputText)
    tts.write_to_fp(audioFilePointer)
    

    pass 

#get audio from the microphone                                                                       
r = sr.Recognizer()                                                                                   

with sr.Microphone() as source:                                                                       
    print("Speak:")                                                                                   
    audio = r.listen(source,10,4)   
    
try:
    print("You said " + r.recognize_google(audio))
    print("asdfasdfasdf not ")
    tts = gTTS(r.recognize_google(audio))
    print("asdfasdfasdf not ")
    tts.save('temp.mp3')
    print("asdfasdfasdf not ")
    #del(tts)
    playsound('temp.mp3',False)
    print("asdfasdfasdf not ")
    
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))


