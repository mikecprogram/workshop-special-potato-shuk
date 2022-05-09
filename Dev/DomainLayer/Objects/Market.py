from operator import is_
import time
import threading

from DomainLayer.Objects.Member import Member
from .Logger import Logger
from .User import User

class Market:
    maxtimeonline = 60 * 10 #10 minutes
    def ___init___(self):
        self._members = []
        self._onlineVisitors = {} #hashmap
        self._onlineDate = {}  # hashmap  used only by can_perform_action,enter
        self._nextToken = -1
        self._enterLock = threading.Lock()
        pass

    #returns boolean, returns if current date < 10Minutes+_onlineDate[token]
    # if #t update _onlineDate[token]
    #this will be checked before each user function
    def can_perform_action(self,token):
        currentTime = time.time()
        if  currentTime - self._onlineDate[token] < maxtimeonline:
            self._onlineDate[token] = currentTime
            return True
        else:
            raise Exception("session time run out")

    #sync me on [enter]
    def enter(self):
        #return token id
        #save token id with a user-guest attached
        self._enterLock.acquire()
        self._nextToken = self._nextToken + 1
        currentToken = self._nextToken
        self._onlineVisitors[self._nextToken] = User(self)
        self._onlineDate[self._nextToken] = time.time()
        self._enterLock.release()
        return currentToken
    def exit(self,token):
        self._onlineDate[token] = 0
        pass
        

    def register(self, username, password, token):
        if self.can_perform_action(token):
            if self.is_exist_member(username):
                if self.is_valid_password(password):
                    hashedPassword = password #TODO: hash this using external class
                    member = Member(username,hashedPassword)
                    pass
    
    def is_valid_password(self, password):  
        if len(password) >= 8:      # need to add constraints on pass TODO
            return True
        else:
            raise Exception("invalid password") # may add some hint about a valid password TODO

    def is_exist_member(self, username):
        if any(member.get_username() == username for member in self._members):
            return True
        else:
            raise Exception("Member already exists!")




    def open_shop(self, token):
        if self.can_perform_action(token):
            pass


    def close_shop(self, token):
        if self.can_perform_action(token):
            pass


        pass


