
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsCategory(Composable):

    def __init__(self, ID, percent, category):
        self.ID = ID
        self.percent = percent
        self.category = category

    def apply(self, user: User, item: StockItem):
        return item.getCategory() == self.category