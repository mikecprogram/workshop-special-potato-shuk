#from .Logger import Logger


class Permissions:

    def __init__(self):
        self._managerAssignment = False  # boolean
        self._ownerAssignment = False  # boolean
        self.RolesInfoReport = False

    def can_assign_manager(self):
        return self._managerAssignment

    def can_assign_owner(self):
        return self._ownerAssignment

    def canGetRolesInfoReport(self):
        return self.RolesInfoReport
