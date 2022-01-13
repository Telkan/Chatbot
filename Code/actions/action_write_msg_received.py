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

# added in order to find py-files in parent-parent dir
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentparentdir)

#added by alex, not sure of working
import actionManager
import ChatManager

class ActionWriteMsgReceived(Action):

     def name(self) -> Text:
         return "action_write_msg_received"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
        domain) -> List:

        contact = tracker.get_slot('contact')
        medium_comm = tracker.get_slot('medium_comm')
        
        msg = "Ok, I am showing you the message from " + str(contact) + " sent through " + str(medium_comm) #TODO

        ########################################################################
        # ACTION MANAGER CODE

        # we dont have an interface
        with actionManager.DATABASE_LOCK:
            text = ChatManager.AM.lookup_message(medium_comm, contact, usertype=contact, last=1)

        # TODO implement an interface

        # interface.add_text(text)
        ########################################################################

        if(str(medium_comm)=="Voicemail"):
            msg = "Sorry, I cannot show a vocal message on screen."

        dispatcher.utter_message(text=msg)
        return []
