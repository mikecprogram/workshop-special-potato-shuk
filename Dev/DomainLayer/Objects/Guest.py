from .Logger import Logger
from .Member import Member
from User import User


class Guest(User):

    def __init__(self, market):
        super().__init__(market)


    def logout(self): # could be removed
        # should do nothing on logout by definition
        pass

    def exit(self, token):  # guest quitting do nothing by definition right now.
        self.clearShoppingCart(token)