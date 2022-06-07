from Dev.DomainLayer.Objects.Policies.Composer import Composer


class policyNot(Composer):

    def __init__(self, c1):
        super.__init__(c1, None)
        self.percent = c1.percent

    def apply(self, user, item):
        return not self.c1.apply(user, item)
