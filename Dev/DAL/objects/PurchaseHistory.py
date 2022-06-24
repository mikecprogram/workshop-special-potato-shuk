from DB import *

class PurchaseHistory(db.Entity):
    purchaseString = Required(str)
    shop = Required("Shop",reverse="purchases_history")
