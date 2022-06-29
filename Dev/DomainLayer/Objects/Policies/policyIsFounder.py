from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsFounder(Composable):

    def __init__(self, ID, percent):
        self.ID = ID
        self.percent = float(percent)

    def apply(self, user: User, item: StockItem):

        if user.isMember():
            return user.getMember().is_founded_shop(item.getShopName())
        return False

    def get_args(self):
        return [None,None]
