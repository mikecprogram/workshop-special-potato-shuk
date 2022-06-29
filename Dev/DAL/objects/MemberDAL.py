from Dev.DAL.objects.DB import *
class MemberDAL(db.Entity):
    foundedShops = Set("ShopDAL",reverse="founder",cascade_delete=True)
    ownedShops = Set("ShopDAL",reverse="owners")
    permissions = Set("PermissionsDAL",reverse="member",cascade_delete=True)
    admin = Optional(int) #0 is not admin else is admin
    username = PrimaryKey(str)
    hashed = Required(str)
    savedCart = Optional("ShoppingCartDAL",cascade_delete=True)
    age = Optional(int)
    assigner =Set("AssignmentDAL",cascade_delete=True)
    assignee =Set("AssignmentDAL",cascade_delete=True)
    delayedNotys = Set("DelayedNotyDAL",cascade_delete=True)
    MembersAcceptedBids = Set("MembersAcceptedBids")
    MembersBids = Set("BidDAL")