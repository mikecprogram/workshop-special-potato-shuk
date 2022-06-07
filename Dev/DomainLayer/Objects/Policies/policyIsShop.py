from Dev.DomainLayer.Objects.Policies.Composable import Composable

class policyIsShop(Composable):

    def __init__(self, percent):
        self.percent = percent

    def apply(self, user):
        return True