from DB import *
class Market(db.Entity):
    maxtimeonline = Required(int)
    admins = Set("Member")
