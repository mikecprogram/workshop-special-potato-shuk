from Dev.DomainLayer.Objects import StockItem
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsItem(Composable):

    def __init__(self, ID, percent, itemname):
        self.ID = ID
        self.percent = float(percent)
        self.itemname = itemname

    def apply(self, user, item: StockItem):
        return item.getName() == self.itemname
