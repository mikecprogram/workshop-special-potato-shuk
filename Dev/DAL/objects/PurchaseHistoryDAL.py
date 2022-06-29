from  Dev.DAL.objects.DB import *

class PurchaseHistoryDAL(db.Entity):
    purchaseString = Optional(str,default='')
    shop = Optional("ShopDAL",reverse="purchases_history")
