from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyHasAmount(Composable):

    def __init__(self, shopname, ID, percent, itemname, amount):
        self.shopname = shopname
        self.ID = ID
        self.percent = float(percent)
        self.itemname = str(itemname)
        self.amount = int(amount)

    def apply(self, user: User, item: StockItem):
        basket = user.getBasketByShop(item.getShopName()).checkBasket()
        for listing in basket:
            if listing['name'] == self.itemname:
                return listing['count'] >= self.amount
        return False

    def toDAL(self):
        return DalPolicy(self.shopname, "simple", self.ID, "hasAmount", self.itemname, self.amount)

    def fromDAL(self, dal: DalPolicy):
        self.__init__(dal.shopname, dal.ID, dal.name, dal.arg1, dal.arg2)
