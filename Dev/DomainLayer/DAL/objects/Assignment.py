#from .Logger import Logger
from DB import *

class Assignment(db.Entity):
    assigner = Required("Member")
    assignee = Required("Member")


