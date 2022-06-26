from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyHasPrice(Composable):

    def __init__(self, shopname, ID, percent, itemname, price):
        self.shopname = shopname
        self.ID = ID
        self.percent = float(percent)
        self.itemname = itemname
        self.price = float(price)

    def apply(self, user: User, item: StockItem):
        if self.itemname == "":
            raw = user.getRawPrice(item.getShopName())
            return raw > self.price
        else:
            basket = user.getBasketByShop(item.getShopName()).checkBasket()
            print(basket)
            print(self.itemname)
            for listing in basket:
                if listing['name'] == self.itemname:
                    return listing['count'] * item.getPrice() >= self.price
            return False

    def toDAL(self):
        return DalPolicy(self.shopname, "simple", self.ID, "hasPrice", self.itemname, self.price)

    def fromDAL(self, dal: DalPolicy):
        self.__init__(dal.shopname, dal.ID, dal.name, dal.arg1, dal.arg2)
