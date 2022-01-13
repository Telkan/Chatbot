import ChatManager
import actionManager
from threading import Thread
import API.check_new_messages as DiscordAPI
import time

# global scope for other functions
CM = ChatManager.ChatManager()                              # create chat manager obj
AM = actionManager.ActionManagerObject(CM)      # create action manager obj

am_server_thread = Thread(target=actionManager.api_message_listener, args=[AM])
am_server_thread.start()

alexa_thread = Thread(target=CM.startComProgram, args=[])   
alexa_thread.start()
time.sleep(10)
AM.add_message( 'DISCORD', date='', 'swebent', 'hi baby, how are you?', phone='null', fromUser=False):
#DiscordAPI.start()
