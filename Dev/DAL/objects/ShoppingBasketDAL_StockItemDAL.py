from  Dev.DAL.objects.DB import *

class ShoppingBasketDAL_StockItemDAL(db.Entity):
    ShoppingBasket = Required("ShoppingBasketDAL")
    StockItemName = Required("StockItemNameDAL")
    count = Required(int)