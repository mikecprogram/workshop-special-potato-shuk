from Dev.DataLayer.DalObject import DalObject


class DalPermission(DalObject):

    def __init__(self, username, shopname, pids):
        self.username = username
        self.shopname = shopname
        self.pides = pids

    def store(self):
        pass