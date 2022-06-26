#from .Logger import Logger
from Dev.DAL.objects.DB import *

class AssignmentDAL(db.Entity):
    assigner = Required("MemberDAL",reverse="assignee")
    assignee = Required("MemberDAL",reverse="assigner")
    shopOwner = Optional("ShopDAL",reverse="owners_assignments")
    shopManager = Optional("ShopDAL",reverse="managers_assignments")




