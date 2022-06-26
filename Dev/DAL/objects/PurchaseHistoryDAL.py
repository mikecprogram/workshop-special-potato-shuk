from  Dev.DAL.objects.DB import *

class PurchaseHistoryDAL(db.Entity):
    id = PrimaryKey(int)
    purchaseString = Required(str)
    shop = Optional("ShopDAL",reverse="purchases_history")
