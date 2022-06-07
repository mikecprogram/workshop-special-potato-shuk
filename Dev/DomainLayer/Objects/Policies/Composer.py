from Dev.DomainLayer.Objects.Policies.Composable import Composable


class Composer(Composable):  # any composed discount that takes 2 composables inherits from Composer (XOR, AND, OR...)

    def __init__(self, ID: int, c1: Composable, c2: Composable):
        super.__init__(ID, c1.percent)
        self.c1 = c1
        self.c2 = c2

    def apply(self, user, item):
        return super.apply(user, item)


