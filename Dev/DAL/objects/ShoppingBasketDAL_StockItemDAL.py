from  Dev.DAL.objects.DB import *

class ShoppingBasketDAL_StockItemDAL(db.Entity):
    ShoppingBasket = Required("ShoppingBasketDAL")
    StockItem = Required("StockItemDAL")
    count = Required(int)