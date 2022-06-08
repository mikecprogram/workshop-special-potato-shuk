from Dev.DomainLayer.Objects.Policies.Composer import Composer


class policyIf(Composer):

    def __init__(self, ID, pred, result):
        self.ID = ID
        self.percent = result.percent
        self.c1 = pred
        self.c2 = result

    def apply(self, user, item):
        result = self.c2.apply(user, item)
        return (not result) or (self.c1.apply(user, item) and result)
