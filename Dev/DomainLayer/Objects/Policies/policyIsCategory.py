from Dev.DomainLayer.Objects import StockItem
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsCategory(Composable):

    def __init__(self, ID, percent, category):
        self.ID = ID
        self.percent = float(percent)
        self.category = category

    def apply(self, user, item: StockItem):
        return item.getCategory() == self.category

    def get_args(self):
        return [str(self.category),None]
