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
		created_time = message.created_time + '*'
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
