from membersController import *
from externalSystems import *
from user import *
class market:
    def __init__(self):
        self._membersController = membersController(self)
        self._activeUsers = []#used for notifications
        self._shops = [] #load
        self._externalSystems = externalSystems(self)
        self._admins = []#load
        self._curr = None
        
    def enter(self):
        self._curr=user(self)
        self._activeUsers.append(self._curr)
        
    def exit(self):
        self._activeUsers.remove(self._curr)
        self._curr=None

    def register(self, username, password):
        if self._curr != None:
            self._curr.register(username, password)
            
    def login(self, username, password):
        if self._curr != None:
            self._curr.login(username, password)
            
    def logout(self):
        if self._curr != None:
            self._curr.logout()
