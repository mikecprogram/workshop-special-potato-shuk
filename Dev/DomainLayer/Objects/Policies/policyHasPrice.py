from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyHasPrice(Composable):

    def __init__(self, ID, percent, itemname, price):
        self.ID = ID
        self.percent = percent
        self.itemname = itemname
        self.price = price

    def apply(self, user: User, item: StockItem):

        if self.itemname == "":
            raw = user.getRawPrice(item.getShopName())
            return raw > self.price
        else:
            basket = user.checkBasket(item.getShopName())
            for name, amount in basket.items():
                if name == self.itemname:
                    return amount * item.getPrice() > self.price
        return False
