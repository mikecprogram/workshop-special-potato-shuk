# from .Logger import Logger
import threading

from Dev.DomainLayer.Objects.ShoppingCart import ShoppingCart
from Dev.DomainLayer.Objects.Permissions import Permissions


class Member:

    def __init__(self, username, hashed, market=None):
        self.founded_shops = {}  # {shopName, Shop}
        self.ownedShops = {}  # {shopname, Shop}
        self.managedShops = {}  # load
        self.permissions = {}  # {shopname, Permissions}
        self.admin = market
        self._username = username
        self._hashed = hashed
        self._savedCart = None
        self._age = None
        self.delayedNoty = []

    def getNotifications(self):
        copy = self.delayedNoty.copy()
        self.delayedNoty = []
        return copy

    def addDelayedNotification(self, message):
        self.delayedNoty.append(message)
    def getAge(self):
        return self._age

    def setAge(self, age):
        if age > 0:
            self._age = age
            return True
        return False

    def is_admin(self):
        return self.admin is not None

    def get_username(self):
        return self._username

    def is_eligible_members(self, shop_name):
        return not (shop_name in self.ownedShops or shop_name in self.managedShops or shop_name in self.founded_shops)

    def addFoundedShop(self, shop):
        self.founded_shops[shop.getShopName()] = shop  ##WATCH OUT!!! founder is treated like owner, but is not an owner!!!

    def isHashedCorrect(self, hashed):
        return True if self._hashed == hashed else False

    def addOwnedShop(self, shop):
        self.ownedShops[shop.getShopName()] = shop

    def deleteOwnedShop(self, shop):
        if shop.getShopName() in self.ownedShops:
            del self.ownedShops[shop.getShopName()]

    def deleteManagedShop(self, shop):
        if shop.getShopName() in self.managedShops:
            del self.managedShops[shop.getShopName()]
            del self.permissions[shop.getShopName()]

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

    def is_founded_shop(self, shopName):
        return shopName in self.founded_shops

    def is_managed_shop(self, shopName):
        return shopName in self.managedShops

    def assign_owner(self, shop_name, memberToAssign):
        if self.is_owned_shop(shop_name):
            self.ownedShops[shop_name].assign_owner(self, memberToAssign)
        elif self.is_founded_shop(shop_name):
            self.founded_shops[shop_name].assign_owner(self, memberToAssign)
        elif self.is_managed_shop(shop_name) and self.can_assign_owner(shop_name):
            self.managedShops[shop_name].assign_owner(self, memberToAssign)
        else:
            raise Exception("Member could not assign an owner to not owned or not managed with special permission shop!")

    def assign_manager(self, shop_name, member_to_assign):
        if self.is_owned_shop(shop_name):
            self.ownedShops[shop_name].assign_manager(self, member_to_assign)
        elif self.is_founded_shop(shop_name):
            self.founded_shops[shop_name].assign_manager(self, member_to_assign)
        elif self.is_managed_shop(shop_name) and self.can_assign_owner(shop_name):
            self.managedShops[shop_name].assign_manager(self, member_to_assign)
        else:
            raise Exception("Member could not assign a manager to not owned or not managed with special permission shop!")
        member_to_assign.permissions[shop_name] = Permissions()

    def openShop(self, shop):
        self.addFoundedShop(shop)

    def getRolesInfoReport(self, shop_name):
        if self.is_founded_shop(shop_name):
            return self.founded_shops[shop_name].getRolesInfoReport()
        elif self.is_owned_shop(shop_name):
            return self.ownedShops[shop_name].getRolesInfoReport()
        elif self.is_managed_shop(shop_name) and self.can_assign_owner(shop_name):
            return self.managedShops[shop_name].getRolesInfoReport()
        else:
            raise Exception("Member could not get info about role in not owned or not managed with special permission shop!")

    def saveShoppingCart(self, cart):
        cart.store()
        self._savedCart = cart

    def dropSavedCart(self):
        self._savedCart = None

    def loadShoppingCart(self, user):
        if self._savedCart is None:
            return ShoppingCart(user)
        else:
            self._savedCart.setUser(user)
            return self._savedCart
    def close_shop(self, shop_name):
        if self.is_founded_shop(shop_name):
            return self.founded_shops[shop_name].close_shop()
        else:
            raise Exception("Member could not close a not owned or not managed with special permission shop!")

    def reopen_shop(self, shop_name):
        if self.is_founded_shop(shop_name):
            return self.founded_shops[shop_name].reopen_shop()
        else:
            raise Exception("Member could not reopen a not owned or not managed with special permission shop!")

    def can_close_shop(self, shop_name):
        return self.permissions[shop_name].can_close_shop()

    def get_inshop_purchases_history(self, shop_name):
        if self.is_founded_shop(shop_name):
            return self.founded_shops[shop_name].get_inshop_purchases_history()
        elif self.is_owned_shop(shop_name):
            return self.ownedShops[shop_name].get_inshop_purchases_history()
        elif self.is_managed_shop(shop_name) and self.can_get_inshop_purchases_history(shop_name):
            return self.managedShops[shop_name].get_inshop_purchases_history()
        else:
            raise Exception("Member could not get inshop purchases history about non owned or non managed with special permission shop!")

    def can_get_inshop_purchases_history(self, shop_name):
        return self.permissions[shop_name].can_get_inshop_purchases_history()

    def can_update_manager_permissions(self, shop_name):
        return self.permissions[shop_name].can_change_shop_manager_permissions()

    def grant_permission(self, permission_code, shop_name, target_manager):
        if self.is_owned_shop(shop_name):
            self.ownedShops[shop_name].grant_permission(permission_code, self._username, target_manager)
        elif self.is_founded_shop(shop_name):
            self.founded_shops[shop_name].grant_permission(permission_code, self._username, target_manager)
        elif self.is_managed_shop(shop_name) and self.can_update_manager_permissions(shop_name):
            self.managedShops[shop_name].grant_permission(permission_code, self._username, target_manager)
        else:
            raise Exception(
                "Member could not grant manager permissions in non owned or non managed with special permission shop!")

    def withdraw_permission(self, permission_code, shop_name, target_manager):
        if self.is_owned_shop(shop_name):
            self.ownedShops[shop_name].withdraw_permission(permission_code, self._username, target_manager)
        elif self.is_founded_shop(shop_name):
            self.founded_shops[shop_name].withdraw_permission(permission_code, self._username, target_manager)
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

    def get_permissions_report(self, shop_name,member_name):
        if self.get_username() == member_name:
            return self.permissions[shop_name].get_permission_report_json()
        elif self.is_owned_shop(shop_name):
            return self.ownedShops[shop_name].get_permission_report(member_name)
        elif self.is_founded_shop(shop_name):
            return self.founded_shops[shop_name].get_permission_report(member_name)
        elif self.is_managed_shop(shop_name) and self.canGetRolesInfoReport(shop_name):
            return self.managedShops[shop_name].get_permission_report(member_name)
        else:
            raise Exception(
                "You do not have permission to see %s permissions in shop %s" % (member_name,shop_name))

    def get_member_info(self):
        output = "Member Name= " + self._username + "\n"
        if len(self.founded_shops) > 0:
            output += "founder for: " + str(list(self.founded_shops.keys())) + " shops\n"
        if len(self.ownedShops) > 0:
            output += "owner for: " + str(list(self.ownedShops.keys())) + " shops\n"
        if len(self.managedShops) > 0:
            output += "manager for: " + str(self.permissions.keys()) + "\n"
        if self.admin is not None:
            output = output + "and he is Admin\n"
        return output

    def delete_shop_owner(self, shop_name, owner_name):
        if self.is_founded_shop(shop_name):
            self.founded_shops[shop_name].delete_owner(self._username, owner_name)
        elif self.is_owned_shop(shop_name):
            self.ownedShops[shop_name].delete_owner(self._username, owner_name)
        else:
            raise Exception(self._username + " isn't owner or owner of shop: " + shop_name)

    def does_have_role(self):
        return (len(self.founded_shops) + len(self.ownedShops) + len(self.managedShops)) > 0 or self.admin is not None

    def get_founder_shops(self):
        return list(self.founded_shops.keys())

    def get_owner_shops(self):
        return list(self.ownedShops.keys())

    def get_manage_shops(self):
        return list(self.permissions.keys())

    def grant_permission(self,permission_code, shop_name, target_manager):
        self.ownedShops[shop_name].grant_permission(permission_code, self._username, target_manager)
        
    def withdraw_permission(self,permission_code, shop_name, target_manager):
        self.ownedShops[shop_name].withdraw_permission(permission_code, self._username, target_manager)
