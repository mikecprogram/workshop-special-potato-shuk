from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsOwner(Composable):

    def __init__(self, ID, percent):
        self.ID = ID
        self.percent = float(percent)

    def apply(self, user: User, item: StockItem):
        return user.isMember() and user.getMember().is_owned_shop(item.getShopName())
