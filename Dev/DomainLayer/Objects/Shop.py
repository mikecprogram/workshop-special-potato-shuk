from DiscountPolicy import DiscountPolicy
from Logger import Logger
import StockItem
import Member
from PurchaseHistory import PurchaseHistory
from Assignment import Assignment
from Stock import Stock
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
        pass

    def get_status(self):
        return self._status

    def isAmount(self, itemid, amount):  # if the store has enough supply
        return True

    def itemExists(self, itemid):
        return True

    def getShopName(self):
        return self._name

    def add_item(self, item: StockItem):
        self._stock.add(item)

    def add_item(self, username, item_name, category, item_desc, item_price, amount):
        if not (username in self._owners.keys()) and not (username in self._managers.keys()):
            return False
        if (amount < 0 or item_price < 0 or item_name == ""):
            return False
        nid = self._stock.getNextId()
        item = StockItem.StockItem(nid, category, item_name, item_desc, amount, None, None, item_price)
        # print(item.toString())
        r = self._stock.addStockItem(item)
        # print (self._stock.search(None,None,None,None,self._name))
        return r

    def remove_item(self, itemid: int):
        self._stock.removeStockItem(itemid)

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
