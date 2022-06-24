from Dev.DomainLayer.Objects.Policies.Composer import *


class policyAnd(Composer):

    def __init__(self, ID, c1, c2):
        self.ID = ID
        self.percent = c1.percent
        self.c1 = c1
        self.c2 = c2

    def apply(self, user, item):
        # print("c1: ",self.c1.getID(),self.c1.apply(user, item),"c2: ",self.c2.getID(),self.c2.apply(user, item),self.ID, self.c1.apply(user, item) and self.c2.apply(user, item))

        return self.c1.apply(user, item) and self.c2.apply(user, item)
