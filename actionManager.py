import json

# Pour la V0 -- simulation
# Trouver un message d'un certain medium/contact
# Trouver un message d'un certain medium/contact a une date donnée

# Pour la V1 -- API
# Informer d'une nouvelle arrivée de message

SMS_file = "DataBases/SMS_DataBase.json"
VM_file = "DataBases/VM_DataBase.json"

SMS_medium = "SMS"
VM_medium = "VOICEMAIL"

# Recevoir MEDIUM + CONTACT + DATE + ACTION


def parseDate(date):
    # date format : "05/01/2022, 15:01:34"
    day = date[0:2]
    month = date[3:5]
    year = date[6:10]
    hours = date[12:14]
    minutes = date[15:17]
    seconds = date[18:20]


def isDateInInterval(mydate, targetDate):



def find_message(medium, contact, date):
    if medium == SMS_medium:
        myfile = open(SMS_file, 'r+')
        data = json.load(myfile)
        rk = 0
        for oneContact in data["SMS_History"]:
            if oneContact['contactname'] == contact:

            rk += 1



parseDate("05/01/2022, 15:01:34")