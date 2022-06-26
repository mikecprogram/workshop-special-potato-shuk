from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsFounder(Composable):

    def __init__(self, shopname, ID, percent):
        self.shopname = shopname
        self.ID = ID
        self.percent = float(percent)

    def apply(self, user: User, item: StockItem):
        if user.isMember():
            return user.getMember().is_founded_shop(item.getShopName())
        return False

    def toDAL(self):
        return DalPolicy(self.percent, self.shopname, "simple", self.ID, "isFounder", None, None)

    def fromDAL(self, dal: DalPolicy):
        self.__init__(dal.shopname, dal.ID, dal.name)
