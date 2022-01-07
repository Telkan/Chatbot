import json


# TO CREATE DEFAULT DATABASE
DB_SMS = {'SMS_History': []}
DB_SMS['SMS_History'].append({
    'contactname': 'voicemail',
    'mobilenumber': '123',
    'messages': [{
        'date': "05/01/2022, 15:01:34",
        'from': "voicemail",
        'text': "You have 1 unread message from mom"
    }]
})
DB_SMS['SMS_History'].append({
    'contactname': "mom",
    'mobilenumber': '0612345678',
    'messages':
    [{
        'date': "02/01/2022, 09:04:52",
        'from': "mom",
        'text': "Howdoyoudoaspaceplease?"
    }, {
        'date': "04/01/2022, 01:12:14",
        'from': "mom",
        'text': "Where are you?"
    }, {
        'date': "04/01/2022, 12:54:48",
        'from': "mom",
        'text': "I can't find my phone, can you call me?"
    }, {
        'date': "04/01/2022, 12:56:12",
        'from': "user",
        'text': "You have it in your hand mom"
    }]
})
with open('SMS_DataBase.json', 'w', encoding='utf-8') as f:
    json.dump(DB_SMS, f, ensure_ascii=False, indent=4)


def write_json(new_data, filename='SMS_DataBase.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["SMS_History"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def createNewContact(contact, message, phonenumber, date):
    structureContact = \
        {
            "contactname": contact,
            "mobilenumber": phonenumber,
            "messages": [{
                'date': date,
                'from': contact,
                'text': message
            }]
        }
    write_json(structureContact)


def add_contact_and_message(contact="unknown", message="null", phonenumber="unknown", date="now",
                            filename="SMS_DataBase.json"):
    myfile = open(filename, 'r+')
    data = json.load(myfile)
    rk = 0
    for oneContact in data["SMS_History"]:
        if oneContact['contactname'] == contact:
            y = {
                'date': date,
                'from': contact,
                'text': message
            }
            data["SMS_History"][rk]['messages'].append(y)
            myfile.seek(0)
            json.dump(data, myfile, indent=4)
            return
        rk += 1
    createNewContact(contact, message, phonenumber, date)


def add_new_response_to_contact(contact="unknown", message="null", date="now", filename="SMS_DataBase.json"):
    myfile = open(filename, 'r+')
    data = json.load(myfile)
    rk = 0
    for oneContact in data["SMS_History"]:
        if oneContact['contactname'] == contact:
            y = {
                'date': date,
                'from': "user",
                'text': message
            }
            data["SMS_History"][rk]['messages'].append(y)
            myfile.seek(0)
            json.dump(data, myfile, indent=4)
            return
        rk += 1


my_contact = "Razmo"
contact_phone = "01.23.45.67.89"
add_contact_and_message(contact=my_contact,
                        message="Yoyoyoyoyoyoyo",
                        phonenumber=contact_phone,
                        date="05/01/2022, 15:15:53")
add_contact_and_message(contact=my_contact,
                        message="I'm a ratz doing rap",
                        date="05/01/2022, 15:16:02")
add_new_response_to_contact(contact=my_contact,
                            message="Don't say \"A fond les bananes\" plz",
                            date="05/01/2022, 15:17:13")

my_contact = "Lucas"
contact_phone = "07.77.46.52.46"
add_contact_and_message(contact=my_contact, message="Here's my phonenumber.",
                        phonenumber=contact_phone,
                        date="02/01/2022, 08:35:46")
add_contact_and_message(contact=my_contact,
                        message="This is an important scheduled message, try to catch it",
                        date="03/01/2022, 23:00:00")
add_new_response_to_contact(contact=my_contact,
                            message="Can you create the SMS Database plz?",
                            date="05/01/2022, 15:17:15")
add_contact_and_message(contact=my_contact,
                        message="No.",
                        date="05/01/2022, 15:18:48")
add_contact_and_message(contact=my_contact,
                        message="Haha, I'm kidding, I created it yesterday :)",
                        date="05/01/2022, 15:18:48")



