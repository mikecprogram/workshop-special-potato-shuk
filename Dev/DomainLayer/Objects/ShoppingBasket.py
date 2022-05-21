from .Logger import Logger


class ShoppingBasket:

    def __init__(self,shoppingCart,shop):
        self.shoppingCart = shoppingCart
        self.shop = shop
        self.stockItems = []#load
    def getItemByName(self, itemName):
        for i in self.stockItems:
            if i[0]==itemName:#ghghj
                return i
        return None
    
    def addItem(self, itemName):
        i = self.getItemByName(itemName)
        if i is None:
            self.stockItems.append([itemName,1])
        else:
            i[1]=i[1]+1

    def removeItem(self, itemName):
        i = self.getItemByName(itemName)
        if i is not None:
            if i[1]==1:
                self.stockItems.remove(i)
            else:
                i[1]=i[1]-1

    def checkBasket(self):
        return self.stockItems

