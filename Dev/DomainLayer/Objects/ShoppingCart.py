##from .Logger import Logger
from ShoppingBasket import ShoppingBasket


class ShoppingCart:

    def __init__(self, user):
        self._user = user
        self._cartPrice = None
        self.shoppingBaskets = {}   # {shopName, ShoppingBasket}

    def getBasketByShop(self, shopname):
        for b in self.shoppingBaskets:
            if b.shop == shopname:
                return b
        return None

    def addItem(self, shopName, itemName):
        b = self.getBasketByShop(shopName)
        if b is None:
            self.shoppingBaskets.append(ShoppingBasket(self, shopName))
        b.addItem(itemName)

    def removeItem(self, shopName, itemName):
        b = self.getBasketByShop(shopName)
        if b is not None:
            b.removeItem(itemName)

    def checkBasket(self, shopName):
        b = self.getBasketByShop(shopName)
        if b is not None:
            return b.checkBasket()
        return None

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
