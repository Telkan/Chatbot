import json


# TO CREATE DEFAULT DATABASE
DB_voicemail = {'voicemail_History': []}
"""DB_voicemail['voicemail_History'].append({
    'contactname': 'voicemail',
    'mobilenumber': '123',
    'messages': [{
        'date': "05/01/2022, 15:01:34",
        'from': "voicemail",
        'text': "welcome.mp3"
        'text_before': null
    }]
})
DB_voicemail['voicemail_History'].append({
    'contactname': "boss",
    'mobilenumber': '0612345678',
    'messages':
    [{
        'date': "05/01/2022, 1O:00:00",
        'from': "boss",
        'text': "boss.mp3"
        'text_before': "boss_voicemail.mp3"
    }          
    ]
})
    
DB_voicemail['voicemail_History'].append({
    'contactname': "mom",
    'mobilenumber': '0666666666',
    'messages':
    [{
        'date': "04/01/2022, 9:30:00",
        'from': "mom",
        'text': ""
    }          
    ]
})"""
with open('Voicemail_DataBase.json', 'w', encoding='utf-8') as f:
    json.dump(DB_voicemail, f, ensure_ascii=False, indent=4)


def write_json(new_data, filename='Voicemail_DataBase.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["voicemail_History"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

def add_contact_and_voicemail(contact="unknown", message="null", message_before="null", phonenumber="", date="", filename="Voicemail_DataBase.json"):
    myfile = open(filename, 'r+')
    data = json.load(myfile)
    rk = 0
    for oneContact in data["voicemail_History"]:
        if oneContact['contactname'] == contact:
            data["voicemail_History"][rk]['messages'].append(message)
            myfile.seek(0)
            json.dump(data, myfile, indent=4)
            return
        rk += 1
    createNewContact(contact, message, message_before, phonenumber, date)


def createNewContact(contact, message, message_before, phonenumber, date):
    structureContact = \
        {
            "contactname": contact,
            "mobilenumber": phonenumber,
            "messages": [{
                'date': date,
                'from': contact,
                'text': message,
                'text_before': message_before
            }]
        }
    write_json(structureContact)

add_contact_and_voicemail(contact="Voicemail", message="welcome.mp3", message_before="", phonenumber="123", date="")
add_contact_and_voicemail(contact="Boss", message="boss.mp3", message_before="boss_voicemail.mp3", phonenumber="06.00.00.00.00", date="05/01/2022, 10:00")
add_contact_and_voicemail(contact="mom", message="mom.mp3", message_before="mom_before.mp3",  phonenumber="06.44.44.44.44",date="05/01/2022, 9:30")


