class user:
    def __init__(self,market):
        self.market=market
        self.state=guest(self)
        self.shoppingCart = shoppingCart(self)

    def regiser(self, username, password):
        pass

    def login(self, username, password):
        pass

    def logout(self):
        pass

