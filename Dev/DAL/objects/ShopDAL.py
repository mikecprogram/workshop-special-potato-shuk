from  Dev.DAL.objects.DB import *
class ShopDAL(db.Entity):
    name = PrimaryKey(str)
    stock = Required("StockDAL",cascade_delete=True)
    isOpen = Required(int,default=1) #0 false other true
    founder = Required("MemberDAL")
    owners = Set("MemberDAL")
    permissions = Set("PermissionsDAL",reverse="shop",cascade_delete=True)
    # purchasePolicy = []
    # discountPolicy = []
    owners_assignments = Set("AssignmentDAL",reverse="shopOwner",cascade_delete=True)
    managers_assignments = Set("AssignmentDAL",reverse="shopManager",cascade_delete=True)
    purchases_history = Required("PurchaseHistoryDAL",cascade_delete=True)
    ShoppingBaskets = Set("ShoppingBasketDAL",cascade_delete=True)
    policy = Set("PolicyDAL",cascade_delete=True)