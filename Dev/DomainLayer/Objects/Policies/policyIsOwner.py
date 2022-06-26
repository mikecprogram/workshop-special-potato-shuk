from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsOwner(Composable):

    def __init__(self, shopnmae, ID, percent):
        self.shopname = shopnmae
        self.ID = ID
        self.percent = float(percent)

    def apply(self, user: User, item: StockItem):
        if user.isMember():
            return user.getMember().is_owned_shop(item.getShopName())
        return False

    def toDAL(self):
        return DalPolicy(self.percent, self.shopname, "simple", self.ID, "isCategory", None, None)

    def fromDAL(self, dal: DalPolicy):
        self.__init__(dal.shopname, dal.ID, dal.name)
