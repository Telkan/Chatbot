import json


# TO CREATE DEFAULT DATABASE
DB_calls = {'calls_History': []}

with open('Calls_DataBase.json', 'w', encoding='utf-8') as f:
    json.dump(DB_calls, f, ensure_ascii=False, indent=4)


def write_json(new_data, filename='Calls_DataBase.json'):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["calls_History"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)

def add_contact_and_call(contact="unknown", message="null", phonenumber="", date="", filename="Calls_DataBase.json"):
    myfile = open(filename, 'r+')
    data = json.load(myfile)
    rk = 0
    for oneContact in data["calls_History"]:
        if oneContact['contactname'] == contact:
            data["calls_History"][rk]['messages'].append(message)
            
            myfile.seek(0)
            json.dump(data, myfile, indent=4)
            return
        rk += 1
    createNewContact(contact, message, phonenumber, date)


def createNewContact(contact, message, phonenumber, date):
    structureContact = \
        {
            "contactname": contact,
            "mobilenumber": phonenumber,
            "messages": [{
                'date': date,
                'from': contact,
                'text': message,
            }]
        }
    write_json(structureContact)

add_contact_and_call(contact="random", message="random1.mp3", phonenumber="", date="06/01/2022, 10:00")
add_contact_and_call(contact="random", message="random2.mp3", phonenumber="", date="07/01/2022, 11:00")
add_contact_and_call(contact="random", message="random3.mp3", phonenumber="", date="08/01/2022, 12:00")
add_contact_and_call(contact="Boss", message="boss.mp3", phonenumber="06.00.00.00.00", date="09/01/2022, 13:00")
add_contact_and_call(contact="dad", message="dad.mp3", phonenumber="06.33.33.33.33", date="10/01/2022, 14:00")
add_contact_and_call(contact="mom", message="mom.mp3", phonenumber="06.44.44.44.44", date="11/01/2022, 15:00")

