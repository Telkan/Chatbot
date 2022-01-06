# speech_regoc not working on mac
#import speech_recognition as sr  
#from gtts import gTTS
#from playsound import playsound

class ChatManager:
    def __init__(self):
        pass

    def textToSpeech(self, outputText):
        print('saying: ' + outputText)  # for illustration
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

    def handle_action_manager_msg(self, medium, sender):
        # read the msg out loud and send it to chatbot

        # TODO send message to chatbot
        msg = "New {} from {}".format(medium, sender)

        # speech 
        self.textToSpeech(msg)
        pass                                                          
    
# in order to get access to actionManager.py in parent dir.
import os, sys
sys.path.insert(1, os.getcwd()) 
import actionManager 

# run local test
if __name__ == "__main__":
    CM = ChatManager() # create chat manager obj

    AM = actionManager.ActionManagerObject(CM) # create action manager obj

    textFromAlex = actionManager.MessageObj('Hi baby!', 'Alex', 'SMS', 'Friday 13th')

    AM.add_message(textFromAlex) 



