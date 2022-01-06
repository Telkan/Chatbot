# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionConfirmNewMsgContent(Action):

     def name(self) -> Text:
         return "action_confirm_new_msg_content"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
        domain) -> List:

        user_msg = tracker.latest_message.get("text")
        contact = tracker.get_slot('contact')
        medium_comm = tracker.get_slot('medium_comm')
        time = tracker.get_slot("time")
        
        if(time=="now"): # not a programmed 
            msg = "Can you confirm that you want to send \"" +  str(user_msg) + "\" to " + str(contact) + " through " + str(medium_comm) + " ?"
        else:
            msg = "Can you confirm that you want to send \"" +  str(user_msg) + "\" to " + str(contact) + " through " + str(medium_comm) + " at " + str(time) + " ?"

        dispatcher.utter_message(text=msg)
        return [SlotSet("message", user_msg)]