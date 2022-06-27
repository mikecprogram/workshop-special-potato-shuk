from Dev.DomainLayer.Objects import StockItem
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyHasPrice(Composable):

    def __init__(self, ID, percent, itemname, price):
        self.ID = ID
        self.percent = float(percent)
        self.itemname = itemname
        self.price = float(price)

    def apply(self, user, item: StockItem):
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
