# from .Logger import Logger
from Dev.DomainLayer.Objects.Permissions import Permissions


class Member:

    def __init__(self, username, hashed, market=None):
        self.foundedShops = []  # load
        self.ownedShops = {}  # {shopname, Shop}
        self.managedShops = []  # load
        self.permissions = {}  # {shopname, Permissions}
        self.assignees = []
        self.admin = market
        self.username = username
        self._hashed = hashed

    def get_username(self):
        return self._username

    def addFoundedShop(self, shop):
        self.foundedShops.append(shop)

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

    def exit(self):
        # store shopping cart in db
        return True

    def is_owned_shop(self, shopName):
        return shopName in self.ownedShops

    def is_managed_shop(self, shopName):
        return shopName in self.managedShops

    def assign_owner(self, shopName, memberToAssign):
        if self.is_owned_shop(shopName):
            self.ownedShops[shopName].assign_owner(self.username, memberToAssign)
        elif self.is_managed_shop(shopName) and self.can_assign_owner(shopName):
            self.managedShops[shopName].assign_owner(self.username, memberToAssign)
        else:
            raise Exception("Member could not assign an owner to not owned or not managed with special permission shop!")

    def assign_manager(self, shopName, memberToAssign):
        if self.is_owned_shop(shopName):
            self.ownedShops[shopName].assign_manager(self.username, memberToAssign)
        elif self.is_managed_shop(shopName) and self.can_assign_owner(shopName):
            self.managedShops[shopName].assign_manager(self.username, memberToAssign)
        else:
            raise Exception("Member could not assign a manager to not owned or not managed with special permission shop!")

    def openShop(self, shop):
        self.addFoundedShop(shop)