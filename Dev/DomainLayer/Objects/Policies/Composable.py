from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects.Persistent import Persistent


class Composable(Persistent):  # any basic discount inherits from Composable (isCategory, isMember, hasAmount...)

    def __init__(self, shopname, ID, percent):
        self.shopname = shopname
        self.ID = 0
        self.percent = 0

    def apply(self, user, item):
        pass

    def getDiscount(self):
        return self.percent

    def getID(self):
        return self.ID

    def __str__(self):
        return "Policy number: " + str(self.ID) + \
               "\npolicy type: " + type(self).__name__ + \
               "\npolicy discount: " + str(self.percent) + \
               "\n"