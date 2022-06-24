from DB import *

class PurchaseHistory(db.Entity):
    purchaseString = Required(str)
