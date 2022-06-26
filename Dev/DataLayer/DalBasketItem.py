from Dev.DataLayer.DalObject import DalObject


class DalBasketItem(DalObject):

    def __init__(self, username, shopname, itemname, count):
        self.usename = username
        self.shopname = shopname
        self.itemname = itemname
        self.count = count

    def store(self):
        pass