from inspect import _emptyé
import speech_recognition as sr  
from gtts import gTTS
from playsound import playsound
import requests
import os, sys
import actionManager 




class ChatManager:
    def __init__(self):
        pass

    def __init__(self) -> None:
        self.api_url = "http://localhost:5005/webhooks/rest/webhook"
        pass
    

    def textToSpeech(self,outputText):
        """
        Plays the audio generated from the text of outputText. This function is blocking everything until it works, and it may be stuck sometimes, sorry :/
        """
        if isinstance(outputText,list):
            if outputText == []:
                self.textToSpeech("I don't know what to say")
                return
            else:
                outputText = outputText[0]["text"]

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


    def listenForVoice(self)->str:
        """
        Gather the audio for the voice recognition software and returns the string of what have been heard
        Can return ERR-<something> to express an error
        """


        r = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:                                                                       
            print("Speak:")                                                                                   
            audio = r.listen(source,10,5)  #Get audio with a timeout of 10s and a max phrase length of 5s
        try:
            print("You said " + r.recognize_google(audio))
            #tts = gTTS(r.recognize_google(audio))
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "ERR-BadAudio"
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))    
            return "ERR-DontWork"                              
    
    def handle_action_manager_msg(self, medium, sender):
        # read the msg out loud and send it to chatbot


        answer = self.sendToChatbot("THE PROTOCOL THAT  WE DECIDE I DON'T REMEMBER SORRY") # TODO create a message using the medium and sender

        #msg = "New {} from {}".format(medium, sender)
        # TODO send message to chatbot
        
        # speech 
        self.textToSpeech(answer)
        pass                                                          

    def sendToChatbot(self, textToSend:str)->str:                
        """
        Send textToSend and return the answer
        """
        self.chatMessage = {"sender": "User", "message": textToSend}
        response = requests.post(self.api_url, json=self.chatMessage)
        print(response.json())
        return response.json()

    def startComProgram(self):
        """
        Main loop of the program, only start this, it takes care of everything, pinky promise :)
        """
        print(self.sendToChatbot("/restart"))
        while True:
            message = self.listenForVoice()
            if "ERR" in message:
                self.textToSpeech("I'm sorry, I didn't get that")    
                continue
            
            if("restart" in message ):
                    print(self.sendToChatbot("/restart"))
                    continue

            if("quit" in message or "exit" in message):
                    return
            
            answer = self.sendToChatbot(message)
            self.textToSpeech(answer)
                              
sys.path.insert(1, os.getcwd()) 

if __name__ == "__main__":
    CM = ChatManager() # create chat manager obj
    AM = actionManager.ActionManagerObject(CM) # create action manager obj
    #textFromAlex = actionManager.MessageObj('Hi baby!', 'Alex', 'SMS', 'Friday 13th')
    #AM.add_message(textFromAlex) 
    CM.startComProgram()