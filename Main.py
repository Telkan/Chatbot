import ChatManager
import actionManager
from threading import Thread
import API.check_new_messages as DiscordAPI

# global scope for other functions
CM = ChatManager.ChatManager()                              # create chat manager obj
AM = actionManager.ActionManagerObject(CM)      # create action manager obj

am_server_thread = Thread(target=actionManager.api_message_listener, args=[AM])
am_server_thread.start()

alexa_thread = Thread(target=CM.startComProgram, args=[])   
#alexa_thread.start()

DiscordAPI.start()
