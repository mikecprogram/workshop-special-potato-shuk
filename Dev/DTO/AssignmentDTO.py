# from .Logger import Logger


class AssignmentDTO:

    def __init__(self, assigner_member, assignee_member):
        self.assigner = assigner_member
        self.assignee = assignee_member
        self.assignmentType = None