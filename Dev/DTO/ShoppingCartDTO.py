
class ShoppingCartDTO:

    def __init__(self, member= None, cartPrice= None, shoppingBaskets= None, id = None):
        self.id = id
        self.member = member
        self.cartPrice = cartPrice
        self.shoppingBaskets = shoppingBaskets
