from Dev.DomainLayer.Objects.Policies.Composable import Composable


class Composer(Composable):  # any composed discount that takes 2 composables inherits from Composer (XOR, AND, OR...)

    def __init__(self, ID: int, c1: Composable, c2: Composable):
        super.__init__(ID, 0)
        self.c1 = c1
        self.c2 = c2

    def apply(self, user, item):
        return super.apply(user, item)

    def __str__(self):
        r = super(Composer, self).__str__()
        return r + "\nchild1: " + self.c1.__str__() + "\nchild2: " + self.c2.__str__()

    def get_args(self):
        return [self.c1,self.c2]