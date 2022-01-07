"""SEND_MESSAGES.PY
This file is a function to send a message (message) in the Chatbot discord server from a
personnal account.
"""
#blablabla
import requests


def send_msg(message):
	payload = {
		'content' : message
	}

	header = {
		'authorization' :  "NjM2ODMwMjUxMDg3MDM2NDQw.YdbFrQ.-CFyzpe3OOCsFYEHdDKhVxCV1_I"
	}

	r = requests.post("https://discord.com/api/v9/channels/928601158392610859/messages", data=payload, headers=header)
