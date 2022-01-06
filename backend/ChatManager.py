# speech_regoc not working on mac
#import speech_recognition as sr  
#from gtts import gTTS
#from playsound import playsound

class ChatManager:
    def __init__(self):
        pass

    def textToSpeech(self, outputText):
        """
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
        """
        pass
    def listenForVoice(self):
        """
        r = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:                                                                       
            print("Speak:")                                                                                   
            audio = r.listen(source,10,7)       
        try:
            print("You said " + r.recognize_google(audio))
            #tts = gTTS(r.recognize_google(audio))
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "Could not understand"
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))    
            return "Could not request results"  
        """

    def handle_action_manager_msg(self, msg, medium, sender, date):
        # read the msg out loud and send it to chatbot
        pass                                                          
    
# test from local file
from actionManager import ActionManagerObject
#from CHATBOT.actionManager import ActionManagerObject
if __name__ == "__main__":
    CM = ChatManager() # create chat manager obj

    AM = ActionManagerObject(CM) # create action manager obj



