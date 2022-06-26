from Dev.DataLayer.DalObject import DalObject


class DalMember(DalObject):

    def __init__(self, username, hashed, age, permissions, delayedNoty):
        self.username = username
        self.hashed = hashed
        self.permissions = permissions
        self.age = age
        self.delayedNoty = delayedNoty

    def store(self):
        pass
