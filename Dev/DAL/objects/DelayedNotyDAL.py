from DB import *

class DelayedNotyDAL(db.Entity):
    notification = Required(str)
    member = Required("MemberDAL")
