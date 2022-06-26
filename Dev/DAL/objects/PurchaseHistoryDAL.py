from  Dev.DAL.objects.DB import *

class PurchaseHistoryDAL(db.Entity):
    purchaseString = Required(str)
    shop = Optional("ShopDAL",reverse="purchases_history")
