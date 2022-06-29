from Dev.DomainLayer.Objects.Policies.Composable import Composable


class policyIsShop(Composable):

    def __init__(self, ID, percent):
        self.ID = ID
        self.percent = float(percent)

    def apply(self, user, item):
        return True

    def get_args(self):
        return [None,None]