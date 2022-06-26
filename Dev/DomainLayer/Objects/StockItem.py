from unicodedata import category


##from .Logger import Logger
import threading

class StockItem:

    def __init__(self, ID=None, category: str=None, name=None, description=None, count=None, purchasepolicy=None, discountpolicy=None, price=None, shopname=None):
        self._id = ID
        self._category = category
        self._desc = description
        self._purchasePolicy = []
        self._discountPolicy = []
        self._name = name
        self._count = count
        self._price = price
        self._shopname = shopname
        self._cache_lock = threading.Lock()

    def aqcuire_cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.acquire()

    def release__cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.release()

    def toString(self):
        return "id: " + str(self._id) + "\ncategory: " + self._category + "\nname: " + self._name + "\namount: " + str(self._count) + "\nprice: " + str(self._price) + "\ndescription: " + self._desc

    def getID(self):
        return self._id

    def getShopName(self):
        return self._shopname

    def addDiscountPolicy(self, discount):
        self._discountPolicy.append(discount)

    def removeDiscountPolicy(self, discount):
        self._discountPolicy.remove(discount)

    def addPurchasePolicy(self, purchase):
        self._purchasePolicy.append(purchase)

    def removePurchasePolicy(self, purchase):
        self._purchasePolicy.remove(purchase)

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

    def setDesc(self, new):
        self._desc = new

    def setPrice(self, new):
        self._price = new

    def canPurchase(self, user):
        return True

    def setAmount(self, amount):
        self._count = amount

    def remove(self, amount):
        if self._count - amount < 0:
            raise "Item cant have negative amount!!!"
        self._count -= amount

    def getTotalDiscount(self, user):
        totaldiscount = 1
        for discount in self._discountPolicy:
            totaldiscount = totaldiscount * discount.getDiscount(user)
        totaldiscount = totaldiscount * self._categroy.getTotalDiscount(user)
        return totaldiscount

    def getDiscountedPrice(self, user):
        totaldiscount = self.getTotalDiscount(user)
        finalPrice = self._price
        if totaldiscount < 1:
            finalPrice = finalPrice * (1 - totaldiscount)
        return finalPrice

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
