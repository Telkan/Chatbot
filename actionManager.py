import json
import threading
import socket
from datetime import datetime
from API.send_messages import send_msg
# Pour la V0 -- simulation
# Trouver un message d'un certain medium/contact
# Trouver un message d'un certain medium/contact a une date donnée

# Pour la V1 -- API
# Informer d'une nouvelle arrivée de message

#SMS_DB = "Databases/SMS/SMS_DataBase.json"
#VM_DB = "Databases/Voicemails/Voicemail_DataBase.json"
#CALLS_DB = "Databases/Calls/Calls_DataBase.json"
GENERAL_DB = "Databases/General_DataBase_test.json"
GENERAL_EVENT_DB = "Databases/General_event_DataBase_test.json"

SMS_medium = "SMS"
VM_medium = "VOICEMAIL"
CALLS_medium = "CALLS"
DISCORD_medium = "DISCORD"

ACTION_MANAGER_SERVER_PORT = 44444

DATABASE_LOCK = threading.Lock()

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
    d1 = datetime(year1, month1, day1, hours1, minutes1, seconds1)
    d2 = datetime(year2, month2, day2, hours2, minutes2, seconds2)
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


def find_message(medium, contact, date='', datetype=1, usertype="all", last=0):
    # Datetype = 0 ==> +-1h
    # Datetype = 1 ==> All day
    # Usertype = "contact", "user", "all"
    # Last = 1 searching last message
    if date == '':   # if we want to create the date of the new msg to add
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y, %H:%M:%S")
        date = dt_string
    
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
        

""" DONT USE this func outside of this file! look at bottom actionManagerObject below instead """
def add_message(medium='', date='', sender='', text='', fromUser=False, phone='null'):

    if medium == '' or sender == '' or text == '': return False # fail check, abort call
    
    if date == '':   # if we want to create the date of the new msg to add
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y, %H:%M:%S")
        date = dt_string
    
    if medium == VM_medium or medium == CALLS_medium:
        if medium == VM_medium: text = 'Databases/Voicemails/' + text

        else: text = 'Databases/Calls/' + text

    with open(GENERAL_DB, 'r+') as file:
        file_data = json.load(file)

        active_db = medium + '_History'     # if its an sms, we work in the sms_db index of the DB

        size = len(file_data[active_db])

        if fromUser:
            new_msg = { 'date':date, 'from':'user', 'text':text}
        else:
            new_msg = { 'date':date, 'from':sender, 'text':text }

        for i in range(size):
            if file_data[active_db][i]["contactname"] == sender:
                file_data[active_db][i]["messages"].append(new_msg)
                break
            if i + 1 == size: #contact doesnt exist in db
                new_contact = {
                        "contactname": sender,
                        "mobilenumber": phone,
                        "messages": [new_msg]}
                
                file_data[active_db].append(new_contact)
                break
        
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)
        return True


class  ActionManagerObject:
    def __init__(self, chat_manager):
        self.cm = chat_manager
        pass        

    def lookup_message(self, medium, contact, date='', datetype=1, usertype="all", last=0):
        # here we have the lookup function

        return find_message(medium.upper(), contact, date, datetype, usertype, last) 
    
    def add_message(self, medium, date='', sender, text, phone='null', fromUser=False):
        # here we have add message logic, db-related etc.
        medium = medium.upper()

        # add msg to db
        if not add_message(medium, date, sender, text, phone, fromUser):
            print('AM: Failed to add new message to db. Abort Chatmanager call.')
            return

        if not fromUser: # code for contacting CM
            self.cm.handle_action_manager_msg(medium, sender)

    def lookup_event(self, args):
        # lookup event db
        pass

    def add_event(self, args):
        # add event to db
        pass

    def send_message(self, medium, contact, text):
        medium = medium.upper()

        self.add_message(medium, '', contact, text,'18',fromUser=True)

        if DISCORD_medium in medium:
            #send_msg(text)
            try:
                send_msg(text)
            except:
                print('AM: sending discord msg failed.')
            break
            
        #elif SMS_medium in medium:
            
        elif VM_medium in medium:
            pass
        elif CALLS_medium in medium:
            pass
        else:
            print('AM: unknown medium, trying to send message: ', medium)



#""" FUNCTION WHICH WILL RECIEVE MESSAGES """
def api_message_listener(AM):

    print('AM_server:--==AM server LIVE==--')

    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM )

    sock.bind(('127.0.0.1', ACTION_MANAGER_SERVER_PORT))    # setup server

    while True:
        # PROTOCOL for sending API messages to this listener         
        # ex incoming msg: DISCORD*null*swebent*null*abo hi
        msg_bytes, address = sock.recvfrom(1024)
        msg = msg_bytes.decode("utf-8")
        els = msg.split('*')

        if len(els)!=5: continue
        print('in AM server:', els)
        with DATABASE_LOCK:
            AM.add_message(els[0], '' if els[1]=='null' else els[1], els[2], els[4])
        return

if __name__ == "__main__":
    #add_message(medium=SMS_medium, sender='Alex', text='testing', phone='074392345',fromUser=True)
    #add_message(medium=DISCORD_medium, sender='Alex', text='testing2', phone='null', fromUser=True)
    #aa = None
    #AM = ActionManagerObject(aa)
    #msgs = AM.lookup_message('Discord', 'swebent',last=1)
    pass
