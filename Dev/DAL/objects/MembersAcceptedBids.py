

from Dev.DAL.objects.DB import *

class MembersAcceptedBids(db.Entity):
    bid = Required("BidDAL")
    members = Set("MemberDAL")
    PrimaryKey(bid)