
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
        # self._discountPolicy = DiscountPolicy()
        # self._purchaseHistory = PurchaseHistory()
        self._owners_assignments = {}
        self._managers_assignments = {}
        self._purchaseLock = threading.Lock()
        self._purchases_history = PurchaseHistory()
        pass
    def getId(self,itemname):
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
        self._purchaseLock.acquire()
        r = self._stock.addStockItem(item)
        self._purchaseLock.release()
        return r

    def add_item(self, username, item_name, category, item_desc, item_price, amount):
        if not (username in self._owners.keys()) and not (username in self._managers.keys()):
            return False
        if (amount < 0 or item_price < 0 or item_name == ""):
            return False
        nid = self._stock.getNextId()
        item = StockItem(nid, category, item_name, item_desc, amount, None, None, item_price)
        # print(item.toString())
        r = self.add_item_lock(item)
        # print (self._stock.search(None,None,None,None,self._name))
        return r

    def remove_item(self, item_name, amount):
        if (amount<0):
            raise Exception('Bad amount to delete')
        self._purchaseLock.acquire()
        r = self._stock.removeStockItem(item_name, amount)
        self._purchaseLock.release()
        return r

    def editItem(self, itemname, new_name, item_desc, item_price):
        if (item_price is not None and item_price < 0) or (new_name is not None and new_name == ""):
            raise Exception('Bad details')
        self._purchaseLock.acquire()
        r = self._stock.editStockItem(itemname, new_name, item_desc, item_price)
        self._purchaseLock.release()
        return r

    def checkAmount(self,item_name, amount):
        if amount < 0:
            raise Exception('Bad amount')
        self._purchaseLock.acquire()
        r = self._stock.checkAmount(item_name, amount)
        self._purchaseLock.release()
        return r

    def update_purchase_policy(self):
        pass

    def update_discount_policy(self):
        pass

    def assign_owner(self, assignerUsername, assignee):
        if assignee.get_username() in self._owners:
            raise Exception("Assignee is already an owner of the shop!")
        # TODO if assigned owner was a manager need to think what to do remove from managers or...
        self._owners[assignee.get_username()] = assignee
        assignee.addOwnedShop(self)
        self.add_assignment(assignerUsername, assignee.get_username(), self._owners_assignments)
        return True

    def assign_manager(self, assignerUsername, assignee):
        if assignee.get_username() in self._managers:
            raise Exception("Assignee is already a manager of the shop!")
        if assignee.get_username() in self._owners:
            raise Exception("Assignee is already an owner of the shop!")

        self._managers[assignee.get_username()] = assignee
        assignee.addManagedShop(self)
        self.add_assignment(assignerUsername, assignee.get_username(), self._managers_assignments)
        return True

    def add_assignment(self, assignerUsername, assigneeUsername, assignment):
        if assignerUsername in assignment:
            assignment[assignerUsername].append(Assignment(assignerUsername, assigneeUsername))
        else:
            assignment[assignerUsername] = [Assignment(assignerUsername, assigneeUsername)]

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
        self._purchaseLock.acquire()

    def releaseReleaseLock(self):
        self._purchaseLock.release()

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


    def grant_permission(self,permission_code, grantor_username, grantee_manager):

        if not self.is_manager(grantee_manager.get_username()):
            raise Exception('Asked grantee member is not a manager of the given shop in market!')
        if not(self.is_owner(grantor_username) and self.is_assignment(grantor_username, grantee_manager.get_username())):
            raise Exception('Owner can only update his assignees permissions!')
        grantee_manager.get_permissions(self._name).add_permission(permission_code)


    def withdraw_permission(self,permission_code, grantor_username, grantee_manager):
        if not self.is_manager(grantee_manager.get_username()):
            raise Exception('Asked member is not a manager of the given shop in market!')
        if not(self.is_owner(grantor_username) and self.is_assignment(grantor_username, grantee_manager.get_username())):
            raise Exception('Owner can only update his assignees permissions!')
        grantee_manager.get_permissions(self._name).remove_permission(permission_code)

    def archive_shopping_basket(self, shooping_basket_report):
        self._purchases_history.append(shooping_basket_report)