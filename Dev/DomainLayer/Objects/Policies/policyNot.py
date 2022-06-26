from Dev.DomainLayer.Objects.Policies.Composer import Composer


class policyNot(Composer):

    def __init__(self, shopname, ID, c1):
        self.shopname = shopname
        self.ID = ID
        self.percent = c1.percent
        self.c1 = c1

    def apply(self, user, item):
        return not self.c1.apply(user, item)
