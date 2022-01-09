# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionConfirmAppointment(Action):
    # mandatory slots : name_appointment, date
    # time is optional

    # initial values :
    #   - name_appointment: null
    #   - date: Today
    #   - time: now

     def name(self) -> Text:
         return "action_confirm_delete_appointment"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain) -> List:

        name_appointment = tracker.get_slot('name_appointment')
        date = tracker.get_slot('date')
        time = tracker.get_slot("time")
        #print("Name appointment: " + str(name_appointment))
        #print("Date: " + str(date))
        #print("Time: " + str(time))

        if(str(name_appointment)=="null" or str(date)=="Today"): #if one of the required slots was not filled
            if(str(name_appointment)=="null"):
                msg = "What is the name of the appointment you want to delete?"
            else:
                if(str(date)=="Today"):
                    msg = "Which day is this appointment scheduled?"
        else: # all mandatory slots are filled
            if(str(time)=="now"):
                msg = "Can you confirm that you want to delete the appointment " + str(name_appointment) + " " + str(date) + "?"
            else:
                msg = "Can you confirm that you want to delete the appointment " + str(name_appointment) + " " + str(date) + " " + str(time) +"?"

        dispatcher.utter_message(text=msg)
        return []