from Dev.DataLayer.DalObject import DalObject


class DalBasket(DalObject):

    def __init__(self, username, shopname, items):
        self.usename = username
        self.shopname = shopname
        self.items = items

    def store(self):
        pass