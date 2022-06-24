from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsFounder(Composable):

    def __init__(self, ID, percent):
        self.ID = ID
        self.percent = percent

    def apply(self, user: User, item: StockItem):
        return user.isMember() and user.getMember().is_founded_shop(item.getShopName())
