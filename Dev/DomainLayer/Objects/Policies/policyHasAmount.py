from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyHasAmount(Composable):

    def __init__(self, ID, percent, itemname, amount):
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