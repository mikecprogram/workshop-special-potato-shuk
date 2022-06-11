from Dev.DomainLayer.Objects.Policies.policyIsShop import policyIsShop
from Dev.DomainLayer.Objects.StockItem import *
from Dev.DomainLayer.Objects.Assignment import Assignment
from Dev.DomainLayer.Objects.Stock import Stock
from Dev.DomainLayer.Objects.PurchaseHistory import PurchaseHistory
import threading

from enum import Enum


class ShopState(Enum):
    Open = 1
    Closed = 0


class Shop():

    def __init__(self, shopName: str, founder):
        self._name = shopName
        self._stock = Stock()
        self._status = ShopState.Open  # need to confirm if we need shop's status such as closed/open. TODO
        self._founder = founder
        self._owners = {founder.get_username(): founder}  # {ownerUsername, Member}
        self._managers = {}  # {managerUsername, Member}
        self._purchasePolicy = []
        self._purchaseLock = threading.Lock()
        self._discountPolicy = []
        self._discountLock = threading.Lock()
        # self._purchaseHistory = PurchaseHistory()
        self._owners_assignments = {}
        self._managers_assignments = {}
        self._purchases_history = PurchaseHistory()
        self._shop_lock = threading.Lock()
        pass

    def getId(self, itemname):
        return self._stock.getId(itemname)

    def get_status(self):
        return self._status

    def isAmount(self, itemid, amount):  # if the store has enough supply
        return True

    def itemExists(self, itemid):
        return True

    def getShopName(self):
        return self._name

    def add_item_lock(self, item: StockItem):
        self._shop_lock.acquire()
        r = self._stock.addStockItem(item)
        self._shop_lock.release()
        return r

    def add_item(self, username, item_name, category, item_desc, item_price, amount):
        if not (username in self._owners.keys()) and not (username in self._managers.keys()):
            return False
        if (amount < 0 or item_price < 0 or item_name == ""):
            return False
        nid = self._stock.getNextId()
        item = StockItem(nid, category, item_name, item_desc, amount, None, None, item_price, self._name)
        # print(item.toString())
        r = self.add_item_lock(item)
        # print (self._stock.search(None,None,None,None,self._name))
        return r

    def remove_item(self, item_name, amount):
        if (amount < 0):
            raise Exception('Bad amount to delete')
        self._shop_lock.acquire()
        r = self._stock.removeStockItem(item_name, amount)
        self._shop_lock.release()
        return r

    def editItem(self, itemname, new_name, item_desc, item_price):
        if (item_price is not None and item_price < 0) or (new_name is not None and new_name == ""):
            raise Exception('Bad details')
        self._shop_lock.acquire()
        r = self._stock.editStockItem(itemname, new_name, item_desc, item_price)
        self._shop_lock.release()
        return r

    def checkAmount(self, item_name, amount):
        if amount < 0:
            raise Exception('Bad amount')
        self._shop_lock.acquire()
        r = self._stock.checkAmount(item_name, amount)
        self._shop_lock.release()
        return r

    def assign_owner(self, assigner_member_object, assignee_member_object):
        if assignee_member_object.get_username() in self._owners:
            raise Exception("Assignee is already an owner of the shop!")
        # TODO if assigned owner was a manager need to think what to do remove from managers or...
        self._owners[assignee_member_object.get_username()] = assignee_member_object
        assignee_member_object.addOwnedShop(self)
        self.add_assignment(assigner_member_object, assignee_member_object, self._owners_assignments)
        return True

    def delete_owner(self, assigner_user_name, assignee_user_name):
        if assignee_user_name not in self._owners:
            raise Exception(assignee_user_name + " is not an owner of the shop:" + self._name)
        self.delete_assignment_owner(assigner_user_name, assignee_user_name, self._owners_assignments)

    def delete_assignment_owner(self, assigner_user_name, assignee_user_name, assignment):
        assignee_member_object = None
        b = False
        if assigner_user_name in assignment:
            for i in assignment[assigner_user_name]:
                if i.assignee.get_username() == assignee_user_name:
                    assignee_member_object = i.assignee
                    assignment[assigner_user_name].remove(i)
                    b = True
                    break
        if not b:
            raise Exception(assigner_user_name + " did not assignee " + assignee_user_name)
        self.recursive_delete(assignee_member_object)

    def recursive_delete(self, member_to_delete):
        if member_to_delete.get_username() in self._owners_assignments:
            for i in self._owners_assignments[member_to_delete.get_username()]:
                self.recursive_delete(i.assignee)
        if member_to_delete.get_username() in self._managers_assignments:
            for i in self._managers_assignments[member_to_delete.get_username()]:
                self.recursive_delete(i.assignee)
        if member_to_delete.get_username() in self._owners_assignments:
            del self._owners_assignments[member_to_delete.get_username()]
        if member_to_delete.get_username() in self._managers_assignments:
            del self._managers_assignments[member_to_delete.get_username()]
        member_to_delete.deleteOwnedShop(self)
        member_to_delete.deleteManagedShop(self)
        if member_to_delete.get_username() in self._owners:
            del self._owners[member_to_delete.get_username()]

    def assign_manager(self, assigner_member_object, assignee_member_object):
        if assignee_member_object.get_username() in self._managers:
            raise Exception("Assignee is already a manager of the shop!")
        if assignee_member_object.get_username() in self._owners:
            raise Exception("Assignee is already an owner of the shop!")

        self._managers[assignee_member_object.get_username()] = assignee_member_object
        assignee_member_object.addManagedShop(self)
        self.add_assignment(assigner_member_object, assignee_member_object, self._managers_assignments)
        return True

    def add_assignment(self, assigner_member_object, assignee_member_object, assignment):
        if assigner_member_object.get_username() in assignment:
            assignment[assigner_member_object.get_username()].append(
                Assignment(assigner_member_object, assignee_member_object))
        else:
            assignment[assigner_member_object.get_username()] = [
                Assignment(assigner_member_object, assignee_member_object)]

    def is_assignment(self, assigner, assignee):
        if assigner in self._owners_assignments:
            return assignee in self._owners_assignments[assigner]
        if assigner in self._managers_assignments:
            return assignee in self._managers_assignments[assigner]

    def close_shop(self):
        if self._status is ShopState.Open:
            self._status = ShopState.Closed
            # TODO add notifying and events system
            pass
            return True
        else:
            raise Exception('Closed shop could not be closed again!')

        pass  # just change state of shop to closed TODO

    def is_manager(self, managerUsername):
        return managerUsername in self._managers

    def is_owner(self, ownerUsername):
        return self._owners[ownerUsername] is not None or self._founder.get_username() == ownerUsername

    def getTotalDiscount(self, user):
        totaldiscount = 1
        for discount in self._discountPolicy:
            totaldiscount = totaldiscount * discount.getDiscount(user)
        return totaldiscount

    def getRolesInfoReport(self):

        report = 'Founder: ' + self._founder + '\n'
        for ownerUsername in self._owners:
            report = report + 'Username: ' + ownerUsername + ' role: owner\n'

        for managerUsername in self._managers:
            report = report + 'Username: ' + managerUsername + ' role: manager\n'

        return report

    def get_shop_report(self):
        return ['Shop name: ' + self._name + '\n' + 'Founder: ' + self._founder.get_username() + '\n',
                self._stock.get_items_report()]

    def aqcuirePurchaseLock(self):
        self._shop_lock.acquire()

    def releaseReleaseLock(self):
        self._shop_lock.release()

    def purchase(self, user, id, amount):
        return True

    def search(self, item_name, category, item_keyword, item_maxPrice):
        r = self._stock.search(item_name, category, item_keyword, item_maxPrice, self._name)
        # print(r)
        return r

    def getItemInfo(self, name):
        return self._stock.getItemInfo(name)

    def get_inshop_purchases_history(self):
        return self._purchases_history.get_string()

    def grant_permission(self, permission_code, grantor_username, grantee_manager):

        if not self.is_manager(grantee_manager.get_username()):
            raise Exception('Asked grantee member is not a manager of the given shop in market!')
        if not (self.is_owner(grantor_username) and self.is_assignment(grantor_username,
                                                                       grantee_manager.get_username())):
            raise Exception('Owner can only update his assignees permissions!')
        grantee_manager.get_permissions(self._name).add_permission(permission_code)

    def withdraw_permission(self, permission_code, grantor_username, grantee_manager):
        if not self.is_manager(grantee_manager.get_username()):
            raise Exception('Asked member is not a manager of the given shop in market!')
        if not (self.is_owner(grantor_username) and self.is_assignment(grantor_username,
                                                                       grantee_manager.get_username())):
            raise Exception('Owner can only update his assignees permissions!')
        grantee_manager.get_permissions(self._name).remove_permission(permission_code)

    def archive_shopping_basket(self, shooping_basket_report):
        self._purchases_history.append(shooping_basket_report)

    def addPurchasePolicy(self, policy):
        self._purchaseLock.acquire()
        self._purchasePolicy.append(policy)
        self._purchaseLock.release()
        return True

    def addDiscountPolicy(self, policy):
        self._discountLock.acquire()
        self._discountPolicy.append(policy)
        self._discountLock.release()
        return True

    def remove_policy(self, ID):
        done = False
        self._discountLock.acquire()
        for d in self._discountPolicy:
            if d.getID() == ID:
                self._discountPolicy.remove(d)
                done = True
        self._discountLock.release()
        self._purchaseLock.acquire()
        for d in self._purchasePolicy:
            if d.getID() == ID:
                self._purchasePolicy.remove(d)
                done = True
        self._purchaseLock.release()
        return done

    def getItemPrice(self, name):
        return self._stock.getItem(name).getPrice()

    def getPolicies(self):
        ret = []
        for p in self._discountPolicy:
            ret.append(["discount", p.getID(), p.getDiscount()])
        for p in self._purchasePolicy:
            ret.append(["purchase", p.getID()])
        return ret

    def validate_purchase(self, user, name):
        item = self._stock.getItem(name)
        for policy in self._purchasePolicy:
            if not policy.apply(user, item):
                return False
        return True

    def calculate_price(self, user, name, amount):
        item = self._stock.getItem(name)
        disc = self.findDiscount(user, item)
        # print(name, disc,item.getPrice()*amount*disc)
        return round(item.getPrice() * amount * disc,3)

    def findDiscount(self, user, item):
        disc = 1
        for policy in self._discountPolicy:
            # print(policy,policy.apply(user, item))
            if policy.apply(user, item):
                d = policy.getDiscount()
                disc *= (1 - d/100)
        return disc
