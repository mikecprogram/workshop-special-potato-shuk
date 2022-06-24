from DB import *

class ShoppingCart(db.Entity):
    Member = Required("Member")
    cartPrice = Optional(int)
    shoppingBaskets = Set("ShoppingBasket")
