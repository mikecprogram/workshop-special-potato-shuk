from Dev.DAL.objects.DB import *

class StockItemNameDAL(db.Entity):
    name = PrimaryKey(str)
    ShoppingBasketDAL_StockItemDAL = Set("ShoppingBasketDAL_StockItemDAL")