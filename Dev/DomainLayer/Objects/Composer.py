import Composable


class Composer(Composable):  # any composed discount that takes 2 composables inherits from Composer (XOR, AND, OR...)

    def apply(self, user):
        return super.apply(user)

    def __init__(self, c1, c2):
        super.__init__()
        self.c1 = c1
        self.c2 = c2
