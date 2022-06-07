# from .Logger import Logger
import threading

from Dev.DomainLayer.Objects.ShoppingCart import ShoppingCart
from Dev.DomainLayer.Objects.Permissions import Permissions


class Member:

    def __init__(self, username, hashed, market=None):
        self.foundedShops = {}  # {shopName, Shop}
        self.ownedShops = {}  # {shopname, Shop}
        self.managedShops = {}  # load
        self.permissions = {}  # {shopname, Permissions}
        self.assignees = []
        self.admin = market
        self._username = username
        self._hashed = hashed
        self._savedCart = None
        self._member_lock=threading.Lock();

    def is_admin(self):
        return self.admin is not None

    def get_username(self):
        return self._username

    def addFoundedShop(self, shop):
        self.foundedShops[shop.getShopName()] = shop

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
    def dropSavedCart(self):
        self._savedCart = None

    def loadShoppingCart(self,user):
        if self._savedCart is None:
            return ShoppingCart(user)
        else:
            self._savedCart.setUser(user)
            return self._savedCart

    def close_shop(self, shopName):
        if self.is_owned_shop(shopName):
            return self.ownedShops[shopName].close_shop()
        elif self.is_managed_shop(shopName) and self.can_close_shop(shopName):
            return self.managedShops[shopName].close_shop()
        else:
            raise Exception("Member could not close a not owned or not managed with special permission shop!")

    def can_close_shop(self, shopName):
        return self.permissions[shopName].can_close_shop()

    def get_inshop_purchases_history(self, shopname):
        if self.is_owned_shop(shopname):
            return self.ownedShops[shopname].get_inshop_purchases_history()
        elif self.is_managed_shop(shopname) and self.can_get_inshop_purchases_history(shopname):
            return self.managedShops[shopname].get_inshop_purchases_history()
        else:
            raise Exception("Member could not get inshop purchases history about non owned or non managed with special permission shop!")

    def can_get_inshop_purchases_history(self, shopname):
        return self.permissions[shopname].can_get_inshop_purchases_history()

    def can_update_manager_permissions(self, shop_name):
        return self.permissions[shop_name].can_change_shop_manager_permissions()

    def grant_permission(self ,permission_code, shop_name, target_manager):
        if self.is_owned_shop(shop_name):
            self.ownedShops[shop_name].grant_permission(permission_code, self._username, target_manager)
        elif self.is_managed_shop(shop_name) and self.can_update_manager_permissions(shop_name):
            self.managedShops[shop_name].grant_permission(permission_code, self._username, target_manager)
        else:
            raise Exception(
                "Member could not grant manager permissions in non owned or non managed with special permission shop!")

    def withdraw_permission(self,permission_code, shop_name, target_manager):
        if self.is_owned_shop(shop_name):
            self.ownedShops[shop_name].withdraw_permission(permission_code, self._username, target_manager)
        elif self.is_managed_shop(shop_name) and self.can_update_manager_permissions(shop_name):
            self.managedShops[shop_name].withdraw_permission(permission_code, self._username, target_manager)
        else:
            raise Exception(
                "Member could not withdraw manager permissions in non owned or non managed with special permission shop!")

    def get_permissions(self, shop_name):
        if shop_name in self.permissions:
            return self.permissions[shop_name]
        else:
            raise Exception('Shop not found!')

    def get_member_info(self):
        self._member_lock.acquire()
        output = "Member Name= " + self._username + "\n"
        if len(self.foundedShops) >0:
            output += "founder for: " + str(list(self.foundedShops.values())) + " shops\n"
        if len(self.ownedShops) > 0:
            output += "owner for: " + str(list(self.ownedShops.values())) + " shops\n"
        if len(self.foundedShops) > 0:
            output += "manager for: " + str(self.permissions) + "\n"
        if self.admin is not None:
            output = output+"and he is Admin\n"
        self._member_lock.release()
        return output
