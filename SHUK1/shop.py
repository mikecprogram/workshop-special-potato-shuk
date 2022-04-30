from ast import For
from SHUK1.stock import stock
from SHUK1.stockItem import stockItem


class shop:
    def __init__(self,market,name,founder):
        self.market = market
        self.name=name
        self.founder = founder
        self.owners = []#load
        self.managers = []#load
        self.purchaseHistory = purchaseHistory(self) #load
        self.discountPolicy = discountPolicy(self)#load
        self.purchasePolicy = purchasePolicy(self)#load
        self.stock = stock(self)

    def addItemToStock(self,item : stockItem, stockNumber):
        self.stock.addItemToStock(item,stockNumber)

    def removeItemFromStock(self,item : stockItem):
        self.stock.removeItemFromStock(item)
        
    def removeItemFromStock(self,itemID):
        self.stock.removeItemFromStock(itemID)

    def getDetails(self):
        return [self.market,self.name,self.founder] #add more details if needed

    def search(self,itemname,category,minItemRating=-1,maxItemRating=-1,minPrice=-1, maxPrice=-1):
        self.stock.search(itemname,category,minItemRating,maxItemRating,minPrice,maxPrice)

    def checkPurchase(self, itemName, itemNumber ,user):

        #check using shop policy here using user

        return self.stock.checkPurchase(itemName, itemNumber)
        
