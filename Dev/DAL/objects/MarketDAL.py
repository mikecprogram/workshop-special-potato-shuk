from DB import *
class MarketDAL(db.Entity):
    maxtimeonline = Required(int)
    admins = Set("MemberDAL")
