import speech_recognition as sr  
from gtts import gTTS
from playsound import playsound
import requests
class ChatManager:

    def __init__(self) -> None:
        self.api_url = "http://localhost:5005/webhooks/rest/webhook"
        pass
    

    def textToSpeech(self,outputText):
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

    def listenForVoice(self):
        r = sr.Recognizer()                                                                                   
        with sr.Microphone() as source:                                                                       
            print("Speak:")                                                                                   
            audio = r.listen(source,10,5)       
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

    def sendToChatbot(self, textToSend):                
        self.chatMessage = {"sender": "Gael", "message": textToSend}
        response = requests.post(self.api_url, json=self.chatMessage)
        print(response.json())
        return response.json()

    def startComProgram(self):
        while True:
            message = self.listenForVoice()
            if "ERR" in message:
                continue  
            answer = self.sendToChatbot(message)
            print(type(answer[0]["text"]))
            self.textToSpeech(answer[0]["text"])

                              
chat = ChatManager()
chat.startComProgram()