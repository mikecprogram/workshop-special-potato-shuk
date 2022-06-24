from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyHasAmount(Composable):

    def __init__(self, ID, percent, itemname, amount):
        self.ID = ID
        self.percent = percent
        self.itemname = itemname
        self.amount = amount

    def apply(self, user: User, item: StockItem):
        basket = user.getBasketByShop(item.getShopName()).checkBasket()
        for item in basket:
            if item['name'] == self.itemname:
                return item['count'] >= self.amount
        return False
