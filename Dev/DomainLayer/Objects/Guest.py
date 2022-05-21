from .Logger import Logger
from .Member import Member
from User import User


class Guest:

    def __init__(self, user: User):
        self._user = user

    def logout(self):
        # should do nothing on logout by definition
        pass

    def login(self, marketid, username, password):
        pass

    def get_username(self):
        return self._username
