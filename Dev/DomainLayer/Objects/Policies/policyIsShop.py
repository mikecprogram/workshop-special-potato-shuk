from Dev.DomainLayer.Objects.Policies.Composable import Composable

class policyIsShop(Composable):

    def __init__(self, ID, percent):
        self.ID = ID
        self.percent = percent

    def apply(self, user, item):
        return True