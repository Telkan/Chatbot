import ChatManager
import actionManager


# global scope for other functions
CM = ChatManager.ChatManager()                              # create chat manager obj
AM = actionManager.ActionManagerObject(CM)      # create action manager obj

CM.startComProgram()                            # start the chatmanager loop (locking)
