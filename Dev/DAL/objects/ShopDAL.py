from  Dev.DAL.objects.DB import *
class ShopDAL(db.Entity):
    name = PrimaryKey(str)
    stock = Required("StockDAL")
    isOpen = Required(int,sql_default=1) #0 false other true
    founder = Required("MemberDAL")
    owners = Set("MemberDAL")
    permissions = Set("PermissionsDAL",reverse="shop")
    # purchasePolicy = []
    # discountPolicy = []
    owners_assignments = Set("AssignmentDAL",reverse="shopOwner")
    managers_assignments = Set("AssignmentDAL",reverse="shopManager")
    purchases_history = Required("PurchaseHistoryDAL")
    ShoppingBaskets = Set("ShoppingBasketDAL")
