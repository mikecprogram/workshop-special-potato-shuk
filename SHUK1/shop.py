from ast import For
from SHUK1.stock import stock
from SHUK1.stockItem import stockItem


class shop:
    def __init__(self,market,founder):
        self.market = market
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