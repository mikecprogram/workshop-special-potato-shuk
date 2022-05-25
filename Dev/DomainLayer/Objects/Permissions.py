#from .Logger import Logger


class Permissions:

    def __init__(self):
        self._managerAssignment = None  # boolean
        self.RolesInfoReport = None

    def can_assign_manager(self):
        return self._managerAssignment

    def canGetRolesInfoReport(self):
        return self.RolesInfoReport
