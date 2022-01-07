"""CHECK_NEW_MESSAGES.PY
This file is checking if there is a new message sent to the Chatbot Discord server, and returns 
it as a string
"""

import discord
import requests
import os
from dotenv import load_dotenv

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
		
		#print(message.content)
		return message.content


client.run(token)
