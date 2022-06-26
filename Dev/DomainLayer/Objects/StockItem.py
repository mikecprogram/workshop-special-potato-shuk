from unicodedata import category


##from .Logger import Logger
from Dev.DataLayer.DalStockItem import DalStockItem
from Dev.DomainLayer.Objects.Persistent import Persistent


class StockItem(Persistent):

    def __init__(self, ID, category: str, name, description, count, price, shopname):
        self._id = ID
        self._category = category
        self._desc = description
        self._name = name
        self._count = count
        self._price = price
        self._shopname = shopname

    def fromDAL(self, dal: DalStockItem):
        self.__init__(dal.id, dal.category, dal.name, dal.desc, dal.count, dal.price, dal.shopname)

    def toDAL(self):
        return DalStockItem( self._id, self._category, self._name, self._desc, self._count,self._price, self._shopname)

    def toString(self):
        return "id: " + str(self._id) + "\ncategory: " + self._category + "\nname: " + self._name + "\namount: " + str(self._count) + "\nprice: " + str(self._price) + "\ndescription: " + self._desc

    def getID(self):
        return self._id

    def getShopName(self):
        return self._shopname

    def getDiscountPolicies(self):
        return self._discountPolicy

    def getPurchasePolicies(self):
        return self._purchasePolicy

    def getName(self):
        return self._name

    def getCount(self):
        return self._count

    def getPrice(self):
        return self._price

    def getDesc(self):
        return self._desc

    def setName(self, new):
        self._name = new
        self.save()

    def setDesc(self, new):
        self._desc = new
        self.save()

    def setPrice(self, new):
        self._price = new
        self.save()

    def canPurchase(self, user):
        return True

    def setAmount(self, amount):
        self._count = amount
        self.save()

    def remove(self, amount):
        if self._count - amount < 0:
            raise "Item cant have negative amount!!!"
        self._count -= amount
        self.save()

    def getCategory(self) -> str:
        return self._category

    def setCategory(self, cat: str):
        self._category = cat

    def get_item_report(self):
        return 'Item: ' + self._name + '\n' + 'Price: ' + self._price + '\n' + 'Amount: ' + self._count + '\n' + 'id: ' + self._id + '\n'

    def get_item_report_dict(self):
        return {'name': self._name, 'price': self._price,
                'amount': self._count,
                'category': self.getCategory(),
                'description': self._desc}
