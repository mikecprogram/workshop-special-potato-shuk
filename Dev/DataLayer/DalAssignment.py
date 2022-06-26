from Dev.DataLayer.DalObject import DalObject


class DalAssignment(DalObject):

    def __init__(self, role, shopname, assigner, assignee):
        self.role = role
        self.shopname = shopname
        self.assigner = assigner
        self.assignee = assignee

    def store(self):
        print(self.role, self.shopname, self.assigner, self.assignee)