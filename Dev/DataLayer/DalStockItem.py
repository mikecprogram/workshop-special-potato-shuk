from Dev.DataLayer.DB import DB
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
        print("shop: "+str(self._shopname)+"\nid: " + str(self._id) + "\ncategory: " + self._category + "\nname: " + self._name + "\namount: " + str(self._count) + "\nprice: " + str(self._price) + "\ndescription: " + self._desc)
        #addr = DB.getDB() we save to DB here


    @property
    def id(self):
        return self._id

    @property
    def category(self):
        return self._category

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def count(self):
        return self._count

    @property
    def price(self):
        return self._price

    @property
    def shopname(self):
        return self._shopname
