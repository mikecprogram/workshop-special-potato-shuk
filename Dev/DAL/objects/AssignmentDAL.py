#from .Logger import Logger
from Dev.DAL.objects.DB import *

class AssignmentDAL(db.Entity):
    assigner = Required("MemberDAL",reverse="assigner")
    assignee = Required("MemberDAL",reverse="assignee")
    shopOwner = Optional("ShopDAL",reverse="owners_assignments")
    shopManager = Optional("ShopDAL",reverse="managers_assignments")




