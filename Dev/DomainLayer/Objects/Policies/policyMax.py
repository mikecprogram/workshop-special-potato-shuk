from Dev.DomainLayer.Objects.Policies.Composer import *


class policyMax(Composer):

    def __init__(self, shopname, ID, c1, c2):
        self.shopname = shopname
        self.ID = ID
        self.percent = max(c1.percent , c2.percent)
        self.c1 = c1
        self.c2 = c2

    def apply(self, user, item):
        return self.c1.apply(user, item) and self.c2.apply(user, item)
