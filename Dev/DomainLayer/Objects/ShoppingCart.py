##from .Logger import Logger
from tkinter import E
from Dev.DomainLayer.Objects.ShoppingBasket import ShoppingBasket
from Dev.DomainLayer.Objects.Shop import Shop

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

    def addItem(self, shop, item_name, amount):
        b = self.getBasketByShop(shop.getShopName())
        if b is None:
            b = ShoppingBasket(self, shop)
            self.shoppingBaskets[shop.getShopName()] = b
        b.addItem(item_name, amount)

    def removeItem(self, shopName, item_name,amount):
        b = self.getBasketByShop(shopName)
        if b is None:
            raise ("removing too from non existant basket!")
        ret = b.removeItem(item_name,amount)
        if not b.checkBasket():
            self.shoppingBaskets.pop(shopName)
        return ret

    def checkBaskets(self):
        ans = []
        for name in self.shoppingBaskets:
            b = self.shoppingBaskets[name]
            ans.append([b.shop.getShopName(),b.checkBasket()])
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
    def purchase(self):
        try:
            for name in self.shoppingBaskets:
                b = self.shoppingBaskets[name]
                b.purchase(self._user)
            return True
        except Exception as e:
            raise e


    def archive_shopping_baskets(self, token):
        for basket in self.shoppingBaskets.values():
            basket.archive(token)
