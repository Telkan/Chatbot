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

class ActionGiveMemoAppointment(Action):

     def name(self) -> Text:
         return "action_give_memo_appointment"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
        domain) -> List:

        
        msg = "Here are your appointments for today " #TODO link to agenda and send back info on today's appointments

        dispatcher.utter_message(text=msg)
        return []
