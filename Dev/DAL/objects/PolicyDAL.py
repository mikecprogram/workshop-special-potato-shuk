from Dev.DAL.objects.DB import *

class PolicyDAL(db.Entity):
    isRoot = Required(int,default = 0)
    type = Required(str)
    shop = Required("ShopDAL")
    ID = Required(int)
    name = Required(str)
    arg1 = Optional(str)
    arg2 = Optional(str)
    percent = Required(int)
