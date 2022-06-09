from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyHasPrice(Composable):

    def __init__(self, ID, percent, age):
        self.ID = ID
        self.percent = percent
        self.age = age

    def apply(self, user: User, item: StockItem):
        return user.getAge() >= self.age
