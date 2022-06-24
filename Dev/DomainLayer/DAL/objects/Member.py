from DB import *
class Member(db.Entity):
    foundedShops = set("Shop")
    ownedShops = set("Shop")
    managedShops = set("Shop")
    permissions = set("Permissions")
    admin = Optional("Market")
    username = Required(str)
    hashed = Required(str)
    savedCart = Optional("ShoppingCart")
    age = Optional(int)
