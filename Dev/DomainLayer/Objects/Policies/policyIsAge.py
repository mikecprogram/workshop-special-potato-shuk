from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyHasPrice(Composable):

    def __init__(self, shopname, ID, percent, age):
        self.shopname = shopname
        self.ID = ID
        self.percent = float(percent)
        self.age = int(age)

    def apply(self, user: User, item: StockItem):
        return user.getAge() >= self.age

    def toDAL(self):
        return DalPolicy(self.percent, self.shopname, "simple", self.ID, "isAge", self.age, None)

    def fromDAL(self, dal: DalPolicy):
        self.__init__(dal.shopname, dal.ID, dal.name, dal.arg1)
