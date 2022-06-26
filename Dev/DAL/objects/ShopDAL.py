from DB import *
class ShopDAL(db.Entity):
    name = Required(str)
    stock = Required("StockDAL")
    isOpen = Required(int) #0 false other true
    founder = Required("MemberDAL")
    owners = Set("MemberDAL")
    permissions = Set("PermissionsDAL",reverse="shop")
    # purchasePolicy = []
    # discountPolicy = []
    owners_assignments = Set("AssignmentDAL",reverse="shopOwner")
    managers_assignments = Set("AssignmentDAL",reverse="shopManager")
    purchases_history = Optional("PurchaseHistoryDAL")
    ShoppingBaskets = Set("ShoppingBasketDAL")
