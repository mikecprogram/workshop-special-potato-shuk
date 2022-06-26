from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsMember(Composable):

    def __init__(self, shopname, ID, percent):
        self.shopname = shopname
        self.ID = ID
        self.percent = float(percent)

    def apply(self, user: User, item: StockItem):
        return user.isMember()

    def toDAL(self):
        return DalPolicy(self.percent, self.shopname, "simple", self.ID, "isCategory", None, None)

    def fromDAL(self, dal: DalPolicy):
        self.__init__(dal.shopname, dal.ID, dal.name)