# from .Logger import Logger


class AssignmentDTO:

    def __init__(self, assigner_member= None, assignee_member= None,id = None):
        self.id = id
        self.assigner = assigner_member
        self.assignee = assignee_member
        self.assignmentType = None
