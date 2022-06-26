from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects.Policies.Composable import Composable
from Dev.DomainLayer.Objects.Policies.policyRecover import policyRecover


class Composer(Composable):  # any composed discount that takes 2 composables inherits from Composer (XOR, AND, OR...)

    def __init__(self, shopname, ID: int, c1: Composable, c2: Composable):
        super.__init__(shopname, ID, 0)
        self.c1 = c1
        self.c2 = c2

    def apply(self, user, item):
        return super.apply(user, item)

    def __str__(self):
        r = super(Composer, self).__str__()
        return r + "\nchild1: " + self.c1.__str__() + "\nchild2: " + self.c2.__str__()

    def toDAL(self):
        return DalPolicy(self.shopname, "complex", self.ID, self.__class__.__name__, self.c1, self.c2)

    def fromDAL(self, dal: DalPolicy):
        self.__init__(dal.shopname, dal.ID, policyRecover.Recover(dal.arg1), policyRecover.Recover(dal.arg1))


