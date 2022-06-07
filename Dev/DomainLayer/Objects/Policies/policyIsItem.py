
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsItem(Composable):

    def __init__(self, ID, percent, itemname):
        self.ID = ID
        self.percent = percent
        self.itemname = itemname

    def apply(self, user: User, item: StockItem):
        return item.getName == self.itemname
