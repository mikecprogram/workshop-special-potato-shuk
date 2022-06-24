from DB import *

class ShoppingBasket(db.Entity):
    shoppingCart = Required("ShoppingCart")
    shop = Required("Shop")
    stockItems = Set("StockItem")
