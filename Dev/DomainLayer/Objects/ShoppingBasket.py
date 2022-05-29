#from .Logger import Logger
from Dev.DomainLayer.Objects.Shop import Shop

class ShoppingBasket:

    def __init__(self, shoppingCart, shop):
        self.shoppingCart = shoppingCart  # is it necessary here?

        self.shop = shop  

        self.stockItems = {}  # load

    def getItemByName(self, itemName):  # refactor and optimize
        for i in self.stockItems:
            if i[0] == itemName:  # ghghj
                return i
        return None

    def addItem(self, itemid,amount):
        if not(self.shop.itemExists(itemid)):
            raise Exception("No such item found in shop")
        if not (itemid in self.stockItems):
            self.stockItems[itemid] = 0
        if not(self.shop.isAmount(itemid,self.stockItems[itemid] +amount)):
            raise Exception("No such amount available in shop")
        self.stockItems[itemid] = self.stockItems[itemid] + amount

    def removeItem(self, itemid,amount): 
        if not(self.shop.itemExists(itemid)):
            raise Exception("No such item found in shop")
        if not(itemid in self.stockItems):
            self.stockItems[itemid] = 0
        if not(self.shop.isAmount(itemid,self.stockItems[itemid] +amount)):
            raise Exception("No such amount available in shop")
        if amount >= self.stockItems[itemid] :
            del self.stockItems[itemid]
        else:
            self.stockItems[itemid] = self.stockItems[itemid] - amount

    def checkBasket(self):
        str = "Different items : %d\n" % len(self.stockItems)
        for id in self.stockItems:
            i = self.stockItems[id]
            str = "%s Item ID: %d\t amount :%i \n" %(str , id,i)
        return str


    def clear(self):
        self.shoppingCart = None
        self.shop = None
        self.stockItems = None
    def purchase(self,user):
        self.shop.aqcuirePurchaseLock()
        try:
            for id in self.stockItems:
                amount = self.stockItems[id]
                if not(self.shop.isAmount(id,amount)):
                    raise Exception("Not enough left from item %d" % id)
                self.shop.purchase(user, id, amount)
                
        except Exception as e:
            self.shop.releaseReleaseLock()
            raise e
        self.stockItems.clear()
        self.shop.releaseReleaseLock()
        return True