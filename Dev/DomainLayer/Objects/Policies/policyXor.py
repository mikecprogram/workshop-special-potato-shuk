from Dev.DomainLayer.Objects.Policies.Composer import Composer


class policyXor(Composer):

    def __init__(self, ID, c1, c2):
        self.ID = ID
        self.percent = c1.percent
        self.c1 = c1
        self.c2 = c2

    def apply(self, user, item):
        return self.c1.apply(user, item) ^ self.c2.apply(user, item)
