from DB import *
class Permissions(db.Entity):
    assignedPermission = set(int)
