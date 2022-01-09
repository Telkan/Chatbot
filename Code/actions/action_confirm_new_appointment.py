# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionConfirmNewAppointment(Action):
    # mandatory slots : name_appointment, date, time

    # initial values :
    #   - name_appointment: null
    #   - date: Today
    #   - time: now

     def name(self) -> Text:
         return "action_confirm_new_appointment"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain) -> List:

        name_appointment = tracker.get_slot('name_appointment')
        date = tracker.get_slot('date')
        time = tracker.get_slot("time")
        #print("Name appointment: " + str(name_appointment))
        #print("Date: " + str(date))
        #print("Time: " + str(time))

        if(str(name_appointment)=="null" or str(date)=="Today" or str(time)=="now"): #if one of the required slots was not filled
            if(str(name_appointment)=="null"):
                msg = "What is the name of your appointment?"
            else:
                if(str(date)=="Today"):
                    msg = "Which day do you want to set your appointment?"
                if(str(time)=="now"):
                    msg = "At what time?"
        else: # all mandatory slots are filled
            msg = "Can you confirm that you want to set the appointment " + str(name_appointment) + " " + str(date) + " " + str(time) +"?"

        dispatcher.utter_message(text=msg)
        return []