from  Dev.DAL.objects.DB import *

class StockDAL(db.Entity):
    #categories = Set("CategoryDAL")
    stockItems = Set("StockItemDAL")
    shop = Optional("ShopDAL")

