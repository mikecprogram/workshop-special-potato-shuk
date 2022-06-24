from DB import *

class PurchaseHistoryDAL(db.Entity):
    purchaseString = Required(str)
    shop = Required("ShopDAL",reverse="purchases_history")
