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
import sys, os
import inspect

# added in order to find py-files in parent-parent dir
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentparentdir)

#added by alex, not sure of working
import actionManager
import Main


class ActionReadMsgReceived(Action):

     def name(self) -> Text:
         return "action_read_msg_received"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
        domain) -> List:

        contact = tracker.get_slot('contact')
        medium_comm = tracker.get_slot('medium_comm')
        
        text = 'Error in action read message received'  # if something wrong
        with actionManager.DATABASE_LOCK:
            text = Main.AM.lookup_message(medium_comm, contact, usertype=contact, last=1)
        print("found:", text)
        msg = "Ok, I am reading the message from " + str(contact) + " sent through " + str(medium_comm) + ". " + str(text) #TODO

        dispatcher.utter_message(text=msg)
        return []
