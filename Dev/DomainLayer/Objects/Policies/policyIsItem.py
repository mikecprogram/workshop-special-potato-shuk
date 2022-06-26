from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsItem(Composable):

    def __init__(self, shopname, ID, percent, itemname):
        self.shopname = shopname
        self.ID = ID
        self.percent = float(percent)
        self.itemname = itemname

    def apply(self, user: User, item: StockItem):
        return item.getName() == self.itemname

    def toDAL(self):
        return DalPolicy(self.percent, self.shopname, "simple", self.ID, "isCategory", self.itemname, None)

    def fromDAL(self, dal: DalPolicy):
        self.__init__(dal.shopname, dal.ID, dal.name, dal.arg1)