import speech_recognition as sr  
from gtts import gTTS
from playsound import playsound

def textToSpeech(outputText):
    tts = gTTS(outputText)
    tts.save('temp.mp3')

    repeat = True
    while repeat:
        try:
            playsound("temp.mp3")
            repeat = False 
        except :
            tts = gTTS(outputText)
            tts.save('temp.mp3')


#get audio from the microphone                                                                       
r = sr.Recognizer()                                                                                   

with sr.Microphone() as source:                                                                       
    print("Speak:")                                                                                   
    audio = r.listen(source,10,4)       
    
try:
    print("You said " + r.recognize_google(audio))
    tts = gTTS(r.recognize_google(audio))
    textToSpeech("You said " + r.recognize_google(audio))    
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))

