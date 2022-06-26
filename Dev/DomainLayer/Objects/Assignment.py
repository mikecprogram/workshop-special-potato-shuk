# from .Logger import Logger
from Dev.DataLayer.DalAssignment import DalAssignment
from Dev.DomainLayer.Objects.Persistent import Persistent


class Assignment(Persistent):

    def __init__(self, role, shopname, assigner_member, assignee_member):
        self.shopname = shopname
        self.assigner = assigner_member
        self.assignee = assignee_member
        self.role = role

    def toDAL(self):
        return DalAssignment(self.role, self.shopname, self.assigner.getUsername(), self.assignee.getUsername())

    def fromDAL(self, dal: DalAssignment):
        pass
