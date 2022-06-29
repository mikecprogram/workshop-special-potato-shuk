from  Dev.DAL.objects.DB import *

class DelayedNotyDAL(db.Entity):
    notification = Required(str)
    member = Required("MemberDAL")
