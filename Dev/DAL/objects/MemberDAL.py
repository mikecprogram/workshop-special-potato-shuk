from DB import *
class MemberDAL(db.Entity):
    foundedShops = Set("ShopDAL",reverse="founder")
    ownedShops = Set("ShopDAL",reverse="owners")
    permissions = Set("PermissionsDAL",reverse="member")
    admin = Optional("MarketDAL")
    username = PrimaryKey(str)
    hashed = Required(str)
    savedCart = Optional("ShoppingCartDAL")
    age = Optional(int)
    assigner =Set("AssignmentDAL")
    assignee =Set("AssignmentDAL")