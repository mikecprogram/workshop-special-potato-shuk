from unicodedata import category

from Dev.DomainLayer.Objects.Category import Category
##from .Logger import Logger


class StockItem:

    def __init__(self, ID ,category, name, description, count, purchasepolicy, discountpolicy,price,shopname):
        self._id = ID
        self._category = category
        self._desc = description
        self._purchasePolicy = []
        self._discountPolicy = []
        self._name = name
        self._count = count
        self._price = price
        self._shopname = shopname
        
    def toString(self):
        return "id: "+str(self._id)+"\ncategory: "+self._category+"\nname: "+self._name+"\namount: "+str(self._count)+"\nprice: "+str(self._price)+"\ndescription: "+self._desc

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
        self._count-=amount

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
            finalPrice = finalPrice * (1-totaldiscount)
        return finalPrice

    def getCategory(self) -> str:
        return self._category
    def setCategory(self,cat):
        self._category = cat
    def removeCategory(self):
        self._category.removeItem(self)
        self._category = None
    def get_item_report(self):
        return 'Item: ' + self._name + '\n' + 'Price: ' + self._price + '\n' + 'Amount: ' + self._count + '\n' + 'id: ' + self._id +'\n'
    def get_item_report_dict(self):
        return {'name' : self._name , 'price' : self._price ,
        'amount' : self._count ,
        'category':self.getCategory(),
        'description':self._desc}
