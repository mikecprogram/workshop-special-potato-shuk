##from .Logger import Logger
# from Guest import *
# from Member import *
# from ShoppingCart import *
from Dev.DomainLayer.Objects.Guest import Guest
from Dev.DomainLayer.Objects.Member import Member
from Dev.DomainLayer.Objects.ShoppingCart import ShoppingCart


class User:
    def __init__(self, market):
        self._market = market
        self._state = Guest(self)
        self._shoppingCart = ShoppingCart(self)
        self._policies=[]

    def isMember(self):
        return isinstance(self._state, Member)

    def getMember(self):
        if self.isMember():
            return self._state
        else:
            raise Exception("This user is not a member")

    def login(self, member):
        if not (self.isMember()):
            self._state = member
            self.clearShoppingCart()
            self._shoppingCart = self._state.loadShoppingCart(self)
            return True
        else:
            raise Exception("Logged in member tried to login again.")

    def logout(self):
        if self.isMember():
            self._state.saveShoppingCart(self._shoppingCart)
            self._state = Guest(self)
            self._shoppingCart = ShoppingCart(self)
        else:
            raise Exception("Cant log out guest")

    def exit(self):
        if self.isMember():
            self.logout()
        else:
            self.clearShoppingCart()

    def openShop(self, shop):
        return self._state.openShop(shop)

    def close_shop(self, shopName):
        return self._state.close_shop(shopName)

    def getAllItems(self):
        return self._shoppingCart.getAllItems()

    def getShops(self):  # ??? wtf
        return self._market.getShops()

    def getShopDetails(self, shopname):
        return self._market.getShopDetails(shopname)

    def search(self, name=None, category=None, keyword=None, maxPrice=None, minItemRating=None, minShopRating=None):
        return self._market.search(name, category, keyword, maxPrice, minItemRating, minShopRating)

    def addToCart(self,shop, item_name,amount):
        self._shoppingCart.addItem(shop, item_name,amount)

    def removeFromCart(self, item_name, shopName,amount):
        return self._shoppingCart.removeItem(shopName, item_name,amount)
    def checkBaskets(self):
        return self._shoppingCart.checkBaskets()
    def checkBasket(self, shopName):
        return self._shoppingCart.checkBasket(shopName)

    def commitPurchase(self):
        if self._market.commitPurchase(self._shoppingCart):
            self._shoppingCart = self.shoppingCart(self)

    def clearShoppingCart(self):
        self._shoppingCart.clear()

    def saveShoppingCart(self):
        self._shoppingCart.store()
        pass

    def assign_owner(self, shopName, memberToAssign):
        self._state.assign_owner(shopName, memberToAssign)

    def assign_manager(self, shopName, memberToAssign):
        self._state.assign_manager(shopName, memberToAssign)
    
    def getRolesInfoReport(self, shopName):
        self._state.getRolesInfoReport(shopName)
    def purchase(self):
        if not(self._shoppingCart.purchase()):
            Exception("Purchase failed for unknown reason")
        if self.isMember():
            self._state.dropSavedCart()
        self.clearShoppingCart()
        self._shoppingCart = ShoppingCart(self)
        return True
    def getUsername(self):
        if self.isMember():
            return self._state.get_username()

    def get_inshop_purchases_history(self, shopname):
        return self._state.get_inshop_purchases_history(shopname)

    def grant_permission(self, permission_code, shop_name, target_manager):
        return self._state.grant_permission(permission_code, shop_name, target_manager)

    def withdraw_permission(self, permission_code, shop_name, target_manager):
        return self._state.withdraw_permission(permission_code, shop_name, target_manager)

    def archive_purchase_cart(self, token):
        self._shoppingCart.archive_shopping_baskets(token)

    def addTempPolicy(self,ID, name, arg1, arg2, percent):
        if arg2 is None:
            self._policies.append([ID, name, arg1, percent])
        else:
            self._policies.append([ID, name, arg1, arg2, percent])
        return True

    def getPolicies(self):
        return self._policies