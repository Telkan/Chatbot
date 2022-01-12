import requests
from flask import Flask,request


def sendToChatbot(textToSend:str)->str:                
        """
        Send textToSend and return the answer
        """
        chatMessage = {"sender": "User", "message": textToSend}
        response = requests.post("http://localhost:5005/webhooks/rest/webhook", json=chatMessage)
        return response.json()

class ChatManager:
    api = Flask(__name__)
    def __init__(self) -> None:
        self.api_url = "http://localhost:5005/webhooks/rest/webhook"
        pass


    @api.route('/', methods=['POST'])
    def post_catchAll():
        shouldEnd = False
        print(request.json)
        if request.json["session"]["new"] == True: 
            text = "What can I do for you?"
            sendToChatbot("/restart")

        elif request.json["request"]["intent"]["name"] == "AMAZON.StopIntent":
            text = "Alright see ya"
            shouldEnd = True

        else:
            text = request.json["request"]["intent"]["slots"]["text"]["value"]  
            text = sendToChatbot(text)
            text = text[0]["text"]
        return {
                    "version": "1.0",
                    "sessionAttributes": {"status": "test"},
                    "response": {
                        "outputSpeech": {
                            "type": "PlainText",
                            "text": text,
                            "playBehavior": "REPLACE_ENQUEUED",
                        },
                        "reprompt": {
                            "outputSpeech": {
                                "type": "PlainText",
                                "text": "Oh gosh darn it, please answer me!",
                                "playBehavior": "REPLACE_ENQUEUED",
                            }
                        },
                        "shouldEndSession": shouldEnd,
                    },
                }

    
    def handle_action_manager_msg(self, medium, sender): # TIME
        # read the msg out loud and send it to chatbot
        answer = self.sendToChatbot("THE PROTOCOL THAT  WE DECIDE I DON'T REMEMBER SORRY") # TODO create a message using the medium and sender

        #msg = "New {} from {}".format(medium, sender)
        # TODO send message to chatbot
        
        # speech 
        self.textToSpeech(answer)
        pass                                                          

    def startComProgram(self):
        """
        Main loop of the program, only start this, it takes care of everything, pinky promise :)
        """
        #print(self.sendToChatbot("/restart"))
        self.api.run(host="localhost") 



if __name__ == "__main__":
    import actionManager 

    CM = ChatManager() # create chat manager obj
    AM = actionManager.ActionManagerObject(CM) # create action manager obj
    CM.startComProgram()
