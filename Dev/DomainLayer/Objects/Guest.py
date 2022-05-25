##from .Logger import Logger


class Guest:

    def __init__(self, user):
        self._user = user

    def exit(self): # does not do anything
        return True

    def assign_owner(self, shopName, memberToAssign):
        raise Exception("Guest could not assign shop owners")

    def exit(self, token):  # guest quitting do nothing by definition right now.
        self.clearShoppingCart(token)

    def assign_manager(self, shopNmae, member):
        raise Exception("Guest could not assign shop managers")

    def getRolesInfoReport(self, shopName):
        raise Exception("Guest could not do this operation")
