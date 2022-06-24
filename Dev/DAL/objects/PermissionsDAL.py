from DB import *

class PermissionsDAL(db.Entity):
    member = Required("MemberDAL")
    shop = Required("ShopDAL")
    permissions_a = Required(int)

