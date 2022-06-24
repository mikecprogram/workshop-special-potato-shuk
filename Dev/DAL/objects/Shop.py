from DB import *
class Shop(db.Entity):
    name = Required(str)
    stock = Required("Stock")
    isOpen = Required(bool) #TODO check and if isn't working change to int
    founder = Required("Member")
    owners = set("Member")
    managers = set("Member")
    purchasePolicy = []
    discountPolicy = []
    owners_assignments = set("Assignment")
    managers_assignments = set("Assignment")
    purchases_history = Required("PurchaseHistory")
