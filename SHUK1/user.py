from guest import *
from market import *
from member import *
from shoppingCart import * 
class user:
    def __init__(self,market):
        self._market=market
        self._state=guest(self)
        self._shoppingCart = shoppingCart(self)

    def register(self, username, password):
        if type(self._state).__name__=="guest":
            self._state.register(username, password)
        else:
            print("already logged in")

    def login(self, username, password):
        if type(self._state).__name__=="guest":
            if (self._state.login(username, password)):
                state=member(self,self._market)
        else:
            print("already logged in")

    def logout(self):
        if type(self._state).__name__!="guest":
            self._state=guest(self)
        else:
            print("already logged out")
