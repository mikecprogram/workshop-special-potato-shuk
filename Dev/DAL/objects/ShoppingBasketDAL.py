from DB import *

class ShoppingBasketDAL(db.Entity):
    shoppingCart = Required("ShoppingCartDAL")
    shop = Required("ShopDAL")
    stockItems = Set("StockItemDAL")
