from DB import *
class Shop(db.Entity):
    name = Required(str)
    stock = Required("Stock")
    isOpen = Required(bool) #TODO check and if isn't working change to int
    founder = Required("Member")
    owners = Set("Member")
    permissions = Set("Permissions",reverse="shop")
    # purchasePolicy = []
    # discountPolicy = []
    owners_assignments = Set("Assignment",reverse="shopOwner")
    managers_assignments = Set("Assignment",reverse="shopManager")
    purchases_history = Optional("PurchaseHistory")
    ShoppingBaskets = Set("ShoppingBasket")

