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


class ActionFeedbackMsgNotSent(Action):

     def name(self) -> Text:
         return "action_feedback_msg_not_sent"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
        domain) -> List:

        contact = tracker.get_slot('contact')
        message = tracker.get_slot('message')
        medium_comm = tracker.get_slot('medium_comm')
        time = tracker.get_slot("time")

        msg = "No worries, I have cancelled the sending of the message."   

        dispatcher.utter_message(text=msg)
        return [SlotSet("contact", "null"), SlotSet("message", "---"),SlotSet("medium_comm", "all"),SlotSet("time", "now")]

