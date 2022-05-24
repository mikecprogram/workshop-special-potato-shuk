from .Logger import Logger


class Permissions:

    def __init__(self):
        self._managerAssignment = None # boolean

    def can_assign_manager(self):
        return self._managerAssignment