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


class ActionSendingNewMsg(Action):

     def name(self) -> Text:
         return "action_sending_new_msg"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
        domain) -> List:

        contact = tracker.get_slot('contact')
        message = tracker.get_slot('message')
        medium_comm = tracker.get_slot('medium_comm')
        time = tracker.get_slot("time")

        if(time=="now"): # not a programmed message
            msg = "Message : \"" + message + "\" sending to " + contact + " through " + medium_comm + "." #TODO
        else:
            msg = "Message : \"" + message + "\" sending to " + contact + " through " + medium_comm + " at " + time + "." #TODO

        dispatcher.utter_message(text=msg)
        
        return [SlotSet("contact", "null"), SlotSet("message", "---"),SlotSet("medium_comm", "all"),SlotSet("time", "now")]

