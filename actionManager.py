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


def find_message(medium, contact, date, datetype=0, usertype="all"):
    # Datetype = 0 ==> +-1h
    # Datetype = 1 ==> All day
    # Usertype = "contact", "user", "default"
    if medium == SMS_medium:
        myfile = open(SMS_file, 'r+')
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


msg = find_message(SMS_medium, "Lucas", "03/01/2022, 23:00:00", datetype=0, usertype="user")
print(msg)
msg = find_message(SMS_medium, "Lucas", "03/01/2022", datetype=1, usertype="contact")
print(msg)
msg = find_message(SMS_medium, "Razmo", "05/01/2022", datetype=1, usertype="user")
print(msg)
msg = find_message(SMS_medium, "Razmo", "05/01/2022", datetype=1, usertype="contact")
print(msg)
msg = find_message(SMS_medium, "Razmo", "05/01/2022", datetype=1, usertype="all")
print(msg)


class  ActionManagerObject:
    def __init__(self, chat_manager):
        self.cm = chat_manager
        pass

    def lookup_message(self,args):
        # here we have the lookup function

        pass

    def add_message(self, args):
        # here we have add message logic, db-related etc.

        # code for contacting CM
        # TODO use self.cm to contact chat manager
        pass