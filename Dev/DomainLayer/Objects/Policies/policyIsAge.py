from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsAge(Composable):

    def __init__(self, ID, percent, age):
        self.ID = ID
        self.percent = float(percent)
        self.age = int(age)

    def apply(self, user: User, item: StockItem):
        return user.getAge() >= self.age

    def get_args(self):
        return [str(self.age),None]
