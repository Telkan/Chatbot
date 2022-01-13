import json
import datetime

# Pour la V0 -- simulation
# Trouver un message d'un certain medium/contact
# Trouver un message d'un certain medium/contact a une date donnée

# Pour la V1 -- API
# Informer d'une nouvelle arrivée de message

SMS_DB = "Databases/SMS/SMS_DataBase.json"
VM_DB = "Databases/Voicemails/Voicemail_DataBase.json"
CALLS_DB = "Databases/Calls/Calls_DataBase.json"
GENERAL_DB = "Databases/General_DataBase.json"

SMS_medium = "SMS"
VM_medium = "VOICEMAIL"
CALLS_medium = "CALLS"
DISCORD_medium = "DISCORD"

def dateInInterval(date1, date2):
    # date format : "05/01/2022, 15:01:34"
    day1 = date1[0:2]
    month1 = date1[3:5]
    year1 = date1[6:10]
    hours1 = int(date1[12:14])
    day2 = date2[0:2]
    month2 = date2[3:5]
    year2 = date2[6:10]
    hours2down = int(date2[12:14])
    hours2up = int(hours2down) + 1
    sameDay = day1 == day2 and month1 == month2 and year1 == year2
    intervalTime = hours2down <= hours1 <= hours2up
    return sameDay and intervalTime


def sameDates(date1, date2):
    day1 = date1[0:2]
    month1 = date1[3:5]
    year1 = date1[6:10]
    day2 = date2[0:2]
    month2 = date2[3:5]
    year2 = date2[6:10]
    return day1 == day2 and month1 == month2 and year1 == year2


def isAfter(date1, date2):
    day1 = int(date1[0:2])
    month1 = int(date1[3:5])
    year1 = int(date1[6:10])
    hours1 = int(date1[12:14])
    minutes1 = int(date1[15:17])
    seconds1 = int(date1[18:20])
    day2 = int(date2[0:2])
    month2 = int(date2[3:5])
    year2 = int(date2[6:10])
    hours2 = int(date2[12:14])
    minutes2 = int(date1[15:17])
    seconds2 = int(date1[18:20])
    d1 = datetime.datetime(year1, month1, day1, hours1, minutes1, seconds1)
    d2 = datetime.datetime(year2, month2, day2, hours2, minutes2, seconds2)
    return d1 > d2


def searchLast(medium, contact):
    myfile = open(GENERAL_DB, 'r+')
    data = json.load(myfile)
    medium_keyword = medium + "_History"
    lastmessage = {
        'date': "01/01/2000, 00:00:00",
        'text': "No message found"
    }
    rk = 0
    for oneContact in data[medium_keyword]:
        if oneContact['contactname'] == contact:
            for struct in data[medium_keyword][rk]["messages"]:
                if isAfter(struct['date'], lastmessage['date']):
                    lastmessage["text"] = struct['text']
                    lastmessage["date"] = struct['date']
        rk += 1
    return lastmessage


def find_message(medium, contact, date="now", datetype=1, usertype="all", last=0):
    # Datetype = 0 ==> +-1h
    # Datetype = 1 ==> All day
    # Usertype = "contact", "user", "all"
    # Last = 1 searching last message
    if last:
        return searchLast(medium, contact)
    if medium == SMS_medium:
        myfile = open(GENERAL_DB, 'r+')
        data = json.load(myfile)
        rk = 0
        messagesFound = []
        for oneContact in data["SMS_History"]:
            if oneContact['contactname'] == contact:
                for struct in data["SMS_History"][rk]['messages']:
                    if datetype == 0:
                        if dateInInterval(struct['date'], date):
                            if usertype == "contact":
                                if struct['from'] == contact:
                                    messagesFound.append(struct['text'])
                            else:
                                if usertype == "user":
                                    if struct['from'] == "user":
                                        messagesFound.append(struct['text'])
                                else:
                                    messagesFound.append(struct['text'])
                    if datetype == 1:
                        if sameDates(struct['date'], date):
                            if usertype == "contact":
                                if struct['from'] == contact:
                                    messagesFound.append(struct['text'])
                            else:
                                if usertype == "user":
                                    if struct['from'] == "user":
                                        messagesFound.append(struct['text'])
                                else:
                                    messagesFound.append(struct['text'])
                myfile.close()
                return messagesFound
            rk += 1
        myfile.close()
    if medium == VM_medium:
        myfile = open(GENERAL_DB, 'r+')
        data = json.load(myfile)
        rk = 0
        messagesFound = []
        for oneContact in data["VM_History"]:
            if oneContact['contactname'] == contact:
                for struct in data["VM_History"][rk]['messages']:
                    if datetype == 0:
                        if dateInInterval(struct['date'], date):
                            messagesFound.append(struct['text'])
                    if datetype == 1:
                        if sameDates(struct['date'], date):
                            messagesFound.append(struct['text'])
                myfile.close()
                return messagesFound
            rk += 1
        myfile.close()
    if medium == CALLS_medium:
        myfile = open(GENERAL_DB, 'r+')
        data = json.load(myfile)
        rk = 0
        messagesFound = []
        for oneContact in data["CALLS_History"]:
            if oneContact['contactname'] == contact:
                for struct in data["CALLS_History"][rk]['messages']:
                    if datetype == 0:
                        if dateInInterval(struct['date'], date):
                            messagesFound.append(struct['text'])
                    if datetype == 1:
                        if sameDates(struct['date'], date):
                            messagesFound.append(struct['text'])
                myfile.close()
                return messagesFound
            rk += 1
        myfile.close()
    return "No message found"

def add_message():
    pass


class  ActionManagerObject:
    def __init__(self, chat_manager):
        self.cm = chat_manager
        pass

    def lookup_message(self, medium, contact, date="now", datetype=1, usertype="all", last=0):
        # here we have the lookup function
        msg = find_message(medium, contact, date, datetype, usertype, last)
        self.cm.handle_action_manager_msg(medium, msg)
    
    def add_message(self, msg):
        # here we have add message logic, db-related etc.

        #TODO add msg to db

        # code for contacting CM
        self.cm.handle_action_manager_msg(msg.medium, msg.sender)

    def lookup_event(self, args):
        # lookup event db
        pass

    def add_event(self, args):
        # add event to db
        pass


if __name__ == "__main__":
    msg = find_message(SMS_medium, "Lucas", "03/01/2022, 23:00:00", datetype=0)
    print(msg)
    msg = find_message(SMS_medium, "Lucas", "03/01/2022", usertype="contact")
    print(msg)
    msg = find_message(SMS_medium, "Razmo", "05/01/2022", usertype="user")
    print(msg)
    msg = find_message(SMS_medium, "Razmo", "05/01/2022", usertype="contact")
    print(msg)
    msg = find_message(SMS_medium, "Razmo", "05/01/2022", usertype="all")
    print(msg)

    msg = find_message(VM_medium, "mom", "05/01/2022")
    print(msg)
    
    msg = find_message(CALLS_medium, "mom", "06/01/2022")
    print(msg)
    msg = find_message(CALLS_medium, "mom", "11/01/2022")
    print(msg)
    
    msg = find_message(SMS_medium, "Razmo", last=1)
    print(msg)