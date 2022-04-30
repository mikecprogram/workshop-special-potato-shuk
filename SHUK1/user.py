from guest import *
from market import *
from member import *
from shoppingCart import *

class user:
    def __init__(self,market):
        self._market=market
        self._state=guest(self)
        self._shoppingCart = shoppingCart(self)

    def register(self, username, password):
        if type(self._state).__name__=="guest":
            self._state.register(self._market._id, username, password)
        else:
            print("already logged in")

    def login(self, username, password):
        if type(self._state).__name__=="guest":
            if (self._state.login(self._market._id, username, password)):
                self.state=member(self,username)
        else:
            print("already logged in")

    def logout(self):
        if type(self._state).__name__!="guest":
            self._state.logout()
            self._state=guest(self)
        else:
            print("already logged out")
    def openShop(self,name):
        if type(self._state).__name__!="guest":
            self._state.openShop(name)
        else:
            print("already logged out")
            

    def getShops(self):
        return self._market.getShops()
    
    def getShopDetails(self,shopname):
        return self._market.getShopDetails(shopname)

    def search(self,name=None,category=None,keyword=None,maxPrice=None,minItemRating=None,minShopRating=None):
        return self._market.search(name,category,keyword,maxPrice,minItemRating,minShopRating)

    def addToCart(self,itemName,shopName):
        self._shoppingCart.addItem(shopName, itemName)

    def removeFromCart(self,itemName,shopName):
        self._shoppingCart.removeItem(shopName, itemName)

    def checkBasket(self, shopName):
        return self._shoppingCart.checkBasket(shopName)

    def commitPurchase(self):
        if self._market.commitPurchase(self._shoppingCart):
            self._shoppingCart=shoppingCart(self)








        
    


