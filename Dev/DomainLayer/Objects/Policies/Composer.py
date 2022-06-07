
from Dev.DomainLayer.Objects.Policies.Composable import Composable


class Composer(Composable):  # any composed discount that takes 2 composables inherits from Composer (XOR, AND, OR...)

    def apply(self, user, item):
        return super.apply(user, item)

    def __init__(self, c1: Composable, c2:Composable):
        super.__init__()
        self.c1 = c1
        self.c2 = c2
