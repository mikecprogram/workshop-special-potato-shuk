from .Logger import Logger
from Guest import *
from Member import *
from ShoppingCart import *


class User:
    def __init__(self, market):
        self._market = market
        self._state = Guest(self)
        self._shoppingCart = ShoppingCart(self)

    def login(self, username, password):
        if (self._state.login(username, password)):
            state = Member(self, username)

    def logout(self):
        self._state = Guest(self)

    def openShop(self, shop):
        self._state.openShop(shop)

    def getAllItems(self):
        return self._shoppingCart.getAllItems()

    def getShops(self):  # ??? wtf
        return self._market.getShops()

    def getShopDetails(self, shopname):
        return self._market.getShopDetails(shopname)

    def search(self, name=None, category=None, keyword=None, maxPrice=None, minItemRating=None, minShopRating=None):
        return self._market.search(name, category, keyword, maxPrice, minItemRating, minShopRating)

    def addToCart(self, itemName, shopName):
        self._shoppingCart.addItem(shopName, itemName)

    def removeFromCart(self, itemName, shopName):
        self._shoppingCart.removeItem(shopName, itemName)

    def checkBasket(self, shopName):
        return self._shoppingCart.checkBasket(shopName)

    def commitPurchase(self):
        if self._market.commitPurchase(self._shoppingCart):
            self._shoppingCart = self.shoppingCart(self)

    def clearShoppingCart(self):
        self._shoppingCart.clear()
