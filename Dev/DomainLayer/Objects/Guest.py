##from .Logger import Logger


class Guest:

    def __init__(self, user):
        self._user = user

    def exit(self): # does not do anything
        return True
