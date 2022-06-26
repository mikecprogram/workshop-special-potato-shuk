from Dev.DataLayer.DalObject import DalObject


class DalStockItem(DalObject):

    def __init__(self, ID, category: str, name, description, count, price, shopname):
        self._shopname = shopname
        self._id = ID
        self._category = category
        self._desc = description
        self._name = name
        self._count = count
        self._price = price

    def store(self):
        pass
