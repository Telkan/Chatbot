# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionConfirmNewMsgContactMedium(Action):

    # mandatory slots : contact, medium_comm
    # optional slot : time if we want to program a message

    # initial values :
    #   - contact : null
    #   - medium_comm : all
    #   - time : now

     def name(self) -> Text:
         return "action_confirm_new_msg_contact_medium"

     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
        domain) -> List:

        contact = tracker.get_slot('contact')
        medium_comm = tracker.get_slot('medium_comm')
        time = tracker.get_slot("time")

        if(medium_comm=="null" or contact=="null"): #if one of the required slots was not filled
            if(medium_comm=="null"):
                msg = "Through which medium of communication?"
            elif(contact=="null"):
                msg = "To which contact should I send it?"
        else: # all mandatory slots are filled
            if(time=="now"): # not a programmed 
                msg = "Can you confirm that you want to send a message to " + contact + " through " + medium_comm + " ?"
            else:
                msg = "Can you confirm that you want to send a message to " + contact + " through " + medium_comm + " at " + time + " ?"

        dispatcher.utter_message(text=msg)
        return []
