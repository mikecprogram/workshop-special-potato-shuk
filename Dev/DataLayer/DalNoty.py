from Dev.DataLayer.DalObject import DalObject


class DalNoty(DalObject):

    def __init__(self, username, noty):
        self.usename = username
        self.noty = noty

    def store(self):
        pass
