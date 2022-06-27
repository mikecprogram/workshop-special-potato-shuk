from  Dev.DAL.objects.DB import *

class PermissionsDAL(db.Entity):
    member = Required("MemberDAL")
    shop = Required("ShopDAL")
    permission = Required(int)

