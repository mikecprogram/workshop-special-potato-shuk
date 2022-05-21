from .Logger import Logger


class ShoppingCart:

    def __init__(self, user):
        self._user = user
        self._shoppingBaskets = None
        self._cartPrice = None
        self.shoppingBaskets = []  #here init baskets ie load from memory

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

    def checkBasket(self, shepName):
        b = self.getBasketByShop(shopName)
        if b is not None:
            return b.checkBasket()
        return None
