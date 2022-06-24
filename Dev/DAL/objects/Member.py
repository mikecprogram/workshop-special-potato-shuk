from DB import *
class Member(db.Entity):
    foundedShops = Set("Shop",reverse="founder")
    ownedShops = Set("Shop",reverse="owners")
    permissions = Set("Permissions",reverse="member")
    admin = Optional("Market")
    username = Required(str)
    hashed = Required(str)
    savedCart = Optional("ShoppingCart")
    age = Optional(int)
    assigner =Set("Assignment")
    assignee =Set("Assignment")