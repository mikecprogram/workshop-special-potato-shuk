

from Dev.DAL.objects.DB import *

class MembersAcceptedBids(db.Entity):
    bid = PrimaryKey("BidDAL")
    members = Set("MemberDAL")
