"""CHECK_NEW_MESSAGES.PY
This file is checking if there is a new message sent to the Chatbot Discord server, and returns 
it as a string
"""

import discord
import requests
import os
from dotenv import load_dotenv
import socket

ACTION_MANAGER_SERVER_PORT = 44444

#Load Discord Bot Token
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.Client()


""" FUNCTION WHICH WILL RECIEVE MESSAGES """
def api_message_listener():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    sock.bind(('127.0.0.1', ACTION_MANAGER_SERVER_PORT))    # setup server

    while True:
        """ PROTOCOL for sending API messages to this listener          """
        """ msg: 'medium*created_time*sender*phone_nr*message_text'     """
        """ ex:  'DISCORD*01/01/2022, 12:00:00*Alex*null*Hello all!'    """

        msg_bytes, address = self.sock.recvfrom(1024)
        print(msg_bytes.decode('utf-8'))

""" code to start it """
from threading import Thread
t1 = Thread(target=api_message_listener, args=[])
t1.start()




@client.event
async def on_ready():
	print(f'{client.user.name} has connected to Discord!')

#Wait for a new Message
@client.event
async def on_message(message):
	
	#Verify that the User is not the Bot itself
	if message.author != client.user:
		
		sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) # socket

		#msg: 'medium*created_time*sender*phone_nr*message_text'    
		medium = 'DISCORD*'
		created_time = message.created_time + '*'	# if this doesnt work I have implemented so we set a date for messages when adding them to the db.
		sender = message.author.name + '*'
		phone_nr = 'null*'
		message_text = message.content

		msg = medium + created_time + sender + phone_nr + message_text
		addr = ('127.0.0.1', 44444)
		sock.sendto(msg, addr)

		return message.content
	else:
		pass


client.run(token)



