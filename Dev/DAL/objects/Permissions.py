from DB import *

class Permissions(db.Entity):
    member = Required("Member")
    shop = Required("Shop")
    permissions_a = Required(int)

