import speech_recognition as sr  
from gtts import gTTS
from playsound import playsound
class ChatManager:


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

    def listenForVoice():
        r = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:                                                                       
            print("Speak:")                                                                                   
            audio = r.listen(source,10,7)       
        try:
            print("You said " + r.recognize_google(audio))
            tts = gTTS(r.recognize_google(audio))
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "Could not understand"
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))    
            return "Could not request results"                                                            
    