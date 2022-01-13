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


class ActionResetAppointment(Action):

     def name(self) -> Text:
         return "action_reset_appointment"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
        domain) -> List:

        name_appointment = tracker.get_slot('name_appointment')
        date = tracker.get_slot('date')
        time = tracker.get_slot('time')
        
        return [SlotSet("name_appointment", "null"), SlotSet("date", "Today"), SlotSet("time", "now")]