import json
import threading
import socket
from datetime import datetime
# Pour la V0 -- simulation
# Trouver un message d'un certain medium/contact
# Trouver un message d'un certain medium/contact a une date donnée

# Pour la V1 -- API
# Informer d'une nouvelle arrivée de message

SMS_DB = "Databases/SMS/SMS_DataBase.json"
VM_DB = "Databases/Voicemails/Voicemail_DataBase.json"
CALLS_DB = "Databases/Calls/Calls_DataBase.json"
GENERAL_DB = "Databases/General_DataBase_test.json"

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

""" DONT USE this func outside of this file! look at bottom actionManagerObject below instead """
def find_message(medium, contact, date, datetype=1, usertype="all"):
    # Datetype = 0 ==> +-1h
    # Datetype = 1 ==> All day
    # Usertype = "contact", "user", "all"
    if medium == SMS_medium:
        myfile = open(SMS_DB, 'r+')
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
        myfile = open(VM_DB, 'r+')
        data = json.load(myfile)
        rk = 0
        messagesFound = []
        for oneContact in data["voicemail_History"]:
            if oneContact['contactname'] == contact:
                for struct in data["voicemail_History"][rk]['messages']:
                    if datetype == 0:
                        if dateInInterval(struct['date'], date):
                            messagesFound.append(struct['text_before'] + "/" + struct['text'])
                    if datetype == 1:
                        if sameDates(struct['date'], date):
                            messagesFound.append(struct['text_before'] + "/" + struct['text'])
                myfile.close()
                return messagesFound
            rk += 1
        myfile.close()
    if medium == CALLS_medium:
        myfile = open(CALLS_DB, 'r+')
        data = json.load(myfile)
        rk = 0
        messagesFound = []
        for oneContact in data["calls_History"]:
            if oneContact['contactname'] == contact:
                for struct in data["calls_History"][rk]['messages']:
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
        

""" DONT USE this func outside of this file! look at bottom actionManagerObject below instead """
def add_message(medium='', date='', sender='', text='', phone='null'):

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

        new_msg = { 'date':date,
                    'from':sender,
                    'text':text}

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


def api_message_listener():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    sock.bind(('127.0.0.1', ACTION_MANAGER_SERVER_PORT))    # setup server

    while True:
        """ PROTOCOL for sending API messages to this listener          """
        """ msg: 'medium*created_time*sender*phone_nr*message_text'     """
        """ ex:  'DISCORD*01/01/2022, 12:00:00*Alex*null*Hello all!'    """

        msg_bytes, address = self.sock.recvfrom(1024)
        print(msg_bytes.decode('utf-8'))


class  ActionManagerObject:
    def __init__(self, chat_manager):
        self.cm = chat_manager
        pass        

    def lookup_message(self,args):
        # here we have the lookup function

        pass
    
    def add_message(self, medium, date, sender, text, phone='null'):
        # here we have add message logic, db-related etc.

        # add msg to db
        if not add_message(medium, date, sender, text, phone):
            print('ActionManagerObj: Failed to add new message to db. Abort Chatmanager call.')
            return

        # code for contacting CM
        self.cm.handle_action_manager_msg(medium, contact)

    def lookup_event(self, args):
        # lookup event db
        pass

    def add_event(self, args):
        # add event to db
        pass

    def send_message():
        pass


if __name__ == "__main__":
    add_message(medium=SMS_medium, sender='Alex', text='get back!', phone='074392345')
    add_message(medium=DISCORD_medium, sender='Alex', text='get back!', phone='074392345')
    
    """
    msg = find_message(SMS_medium, "Lucas", "03/01/2022, 23:00:00", datetype=0, usertype="user")
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
    """
