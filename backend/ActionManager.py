import socket
from backend.APIs import SMSAPI

class ActionManager:
    def __init__(self):
        #define apis to be listened to
        self.sms = SMSAPI()

        # start threads for every api
        pass
        
    def handle_incoming_data(self, msgType, msg):
        
        switch msgType:
            case 'SMS':
                break

        pass

    pass


# just for testing
class chatbot_action_object:
    def __init__(self):
        pass

    def handleSMS(self, text):
        print("sending sms '" + text + "' to chatbot...")