# from .Logger import Logger
from ShoppingCart import ShoppingCart
from Permissions import Permissions


class Member:

    def __init__(self, username, hashed, market=None):
        self.foundedShops = {}  # {shopName, Shop}
        self.ownedShops = {}  # {shopname, Shop}
        self.managedShops = []  # load
        self.permissions = {}  # {shopname, Permissions}
        self.assignees = []
        self.admin = market
        self._username = username
        self._hashed = hashed
        self._savedCart = None

    def get_username(self):
        return self._username

    def addFoundedShop(self, shop):
        self.foundedShops[shop.getShopName()] = shop
        self.ownedShops[shop.getShopName()] = shop

    def isHashedCorrect(self, hashed):
        return True if self._hashed == hashed else False

    def addOwnedShop(self, shop):
        self.ownedShops[shop.getShopName()] = shop

    def addManagedShop(self, shop):
        self.managedShops[shop.getShopName()] = shop
        self.permissions[shop.getShopName()] = Permissions()

    def can_assign_manager(self, shopname):
        return self.permissions[shopname].can_assign_manager()

    def can_assign_owner(self, shopname):
        return self.permissions[shopname].can_assign_owner()

    def canGetRolesInfoReport(self, shopname):
        return self.permissions[shopname].canGetRolesInfoReport()

    def is_owned_shop(self, shopName):
        return shopName in self.ownedShops

    def is_managed_shop(self, shopName):
        return shopName in self.managedShops

    def assign_owner(self, shopName, memberToAssign):
        if self.is_owned_shop(shopName):
            self.ownedShops[shopName].assign_owner(self._username, memberToAssign)
        elif self.is_managed_shop(shopName) and self.can_assign_owner(shopName):
            self.managedShops[shopName].assign_owner(self._username, memberToAssign)
        else:
            raise Exception("Member could not assign an owner to not owned or not managed with special permission shop!")

    def assign_manager(self, shopName, memberToAssign):
        if self.is_owned_shop(shopName):
            self.ownedShops[shopName].assign_manager(self._username, memberToAssign)
        elif self.is_managed_shop(shopName) and self.can_assign_owner(shopName):
            self.managedShops[shopName].assign_manager(self._username, memberToAssign)
        else:
            raise Exception("Member could not assign a manager to not owned or not managed with special permission shop!")

    def openShop(self, shop):
        self.addFoundedShop(shop)

    def getRolesInfoReport(self, shopName):
        if self.is_owned_shop(shopName):
            return self.ownedShops[shopName].getRolesInfoReport()
        elif self.is_managed_shop(shopName) and self.can_assign_owner(shopName):
            return self.managedShops[shopName].getRolesInfoReport()
        else:
            raise Exception("Member could not get info about role in not owned or not managed with special permission shop!")
    def saveShoppingCart(self, cart):
        cart.store()
        self._savedCart = cart
        
    def loadShoppingCart(self,user):
        if self._savedCart is None:
            return ShoppingCart(user)
        else:
            self._savedCart.setUser(user)
            return self._savedCart
