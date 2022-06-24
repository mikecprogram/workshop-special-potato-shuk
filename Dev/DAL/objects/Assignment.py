#from .Logger import Logger
from DB import *

class Assignment(db.Entity):
    assigner = Required("Member",reverse="assignee")
    assignee = Required("Member",reverse="assigner")
    shopOwner = Optional("Shop",reverse="owners_assignments")
    shopManager = Optional("Shop",reverse="managers_assignments")


