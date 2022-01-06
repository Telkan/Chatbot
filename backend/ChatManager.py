from inspect import _empty
import speech_recognition as sr  
from gtts import gTTS
from playsound import playsound
import requests
class ChatManager:

    def __init__(self) -> None:
        self.api_url = "http://localhost:5005/webhooks/rest/webhook"
        pass
    

    def textToSpeech(self,outputText:str):
        """
        Plays the audio generated from the text of outputText. This function is blocking everything until it works, and it may be stuck sometimes, sorry :/
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
            tts = gTTS(r.recognize_google(audio))
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "ERR-BadAudio"
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))    
            return "ERR-DontWork"                              

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
            if answer != []:
                self.textToSpeech(answer[0]["text"])
            else:
                self.textToSpeech("I don't know what to say")

                              
chat = ChatManager()
chat.startComProgram()