##from .Logger import Logger
from ShoppingBasket import ShoppingBasket
import Shop

class ShoppingCart:

    def __init__(self, user):
        self._user = user
        self._cartPrice = None
        self.shoppingBaskets = {}   # {shopName, ShoppingBasket}

    def getBasketByShop(self, shopname):
        for b in self.shoppingBaskets:
            if b == shopname:
                return self.shoppingBaskets[b]
        return None

    def addItem(self, shopName, itemid,amount):
        b = self.getBasketByShop(shopName)
        if b is None:
            b = ShoppingBasket(self, Shop.Shop(shopName,None))
            self.shoppingBaskets[shopName] = b
        b.addItem(itemid,amount)

    def removeItem(self, shopName, itemid,amount):
        b = self.getBasketByShop(shopName)
        if b is None:
            b = ShoppingBasket(self, Shop(shopName,None))
            self.shoppingBaskets[shopName] = b
        b.removeItem(itemid,amount)

    def checkBaskets(self):
        ans = ""
        for name in self.shoppingBaskets:
            b = self.shoppingBaskets[name]
            ans = "%s from shop %s: \n %s\n"%(ans,b.shop.getShopName(),b.checkBasket())
        if ans == "":
            return "Basket is empty"
        else:
            return ans

    def clear(self):
        self._user = None
        self._cartPrice = None
        for shop in self.shoppingBaskets:
            self.shoppingBaskets[shop].clear()

    def store(self):
        self._user = None
        pass         # TODO store the the shopping cart at DB
    def setUser(self,user):
        self._user = user
