from DB import *

class ShoppingBasketDAL(db.Entity):
    shoppingCart = Required("ShoppingCartDAL")
    shop = Required("ShopDAL")
    ShoppingBasketDAL_StockItemDAL = Set("ShoppingBasketDAL_StockItemDAL")
