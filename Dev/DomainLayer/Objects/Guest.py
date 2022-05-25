##from .Logger import Logger


class Guest:

    def __init__(self, user):
        self._user = user

    def exit(self): # does not do anything
        return True

    def assign_owner(self, shopName, memberToAssign):
        raise Exception("Guest could not assign shop owners!")

    def assign_manager(self, shopNmae, member):
        raise Exception("Guest could not assign shop managers!")

    def openShop(self, shop):
        raise Exception("Guest could not open a shop!")
