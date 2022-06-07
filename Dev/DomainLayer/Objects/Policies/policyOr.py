from Dev.DomainLayer.Objects.Policies.Composer import Composer


class policyOr(Composer):

    def __init__(self, c1, c2, percent):
        super.__init__(c1, c2)
        self.percent = percent

    def apply(self, user, item):
        return self.c1.apply(user, item) or self.c2.apply(user, item)