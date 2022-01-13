# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import inspect
import sys
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os

# added in order to find py-files in parent-parent dir
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentparentdir)

#added by alex, not sure of working
import actionManager

import Main

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
            msg = "Message : \"" + str(message) + "\" sending to " + str(contact) + " through " + str(medium_comm) + "." #TODO
        else:
            msg = "Message : \"" + str(message) + "\" sending to " + str(contact) + " through " + str(medium_comm) + " at " + str(time) + "." #TODO
        
        # not sure if we have functionality to send messages at specific times :S, or I understand something wrong
        if time=='now':
            with actionManager.DATABASE_LOCK:
                Main.AM.send_message( str(medium_comm),  str(contact),  str(message)) # function declared but not implemented
        else:
            # to be implemented (aka never)
            pass        


        dispatcher.utter_message(text=msg)
        
        return [SlotSet("contact", "null"), SlotSet("message", "---"),SlotSet("medium_comm", "all"),SlotSet("time", "now")]

