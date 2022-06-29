from Dev.DomainLayer.Objects.Policies.policyIsShop import policyIsShop
from Dev.DomainLayer.Objects.StockItem import StockItem
from Dev.DomainLayer.Objects.Assignment import Assignment,t
from Dev.DomainLayer.Objects.Stock import Stock
from Dev.DomainLayer.Objects.PurchaseHistory import PurchaseHistory
notplugin = None
import threading


class Shop():

    def __init__(self, shop_name, founder=None, notificationPlugin=None,save = True):
        if notificationPlugin is not None:
            notplugin = notificationPlugin
        self._name = shop_name
        self._stock = Stock(shop_name,save)
        self._is_open = True  # need to confirm if we need shop's status such as closed/open. TODO
        self._founder = founder
        self._policies = [] #temp
        self._owners = {}  # {ownerUsername, Member} (ò_ó)!!!!!!!!!!!!!!!!!
        self._managers = {}  # {managerUsername, Member}
        self._purchasePolicies = []
        self._purchaseLock = threading.Lock()
        self._discountPolicies = []
        self._discountLock = threading.Lock()
        # self._purchaseHistory = PurchaseHistory()
        self._owners_assignments = {}
        self._managers_assignments = {}
        self._purchases_history = PurchaseHistory(save = save)
        self._shop_lock = threading.Lock()
        self.notificationPlugin = notificationPlugin
        self._cache_lock = threading.Lock()

    def aqcuire_cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.acquire()

    def release__cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.release()
    def getId(self, itemname):
        return self._stock.getId(itemname)

    def isOpen(self):
        return self._is_open

    def isAmount(self, itemname, amount):  # if the store has enough supply
        return self._stock.isAmount(itemname, amount)

    def itemExists(self, itemname):
        return self._stock.itemExists(itemname)

    def getShopName(self):
        return self._name

    def add_item(self, username: str, item_name: str, category: str, item_desc: str, item_price: float, amount: int):
        item_name = item_name.strip()
        item_desc = item_desc.strip()
        amount = int(amount)
        item_price = float(item_price)

        if amount < 0:
            raise Exception('Amount of item can not be negative')
        if item_price < 0:
            raise Exception('Price of item can not be negative')
        if item_name == "" or item_name is None:
            raise Exception('Item name must not be null')
        if (username != self._founder.get_username()) and not (username in self._owners.keys()) and not (username in self._managers.keys()):
            raise Exception('You do not have the sufficient permissions to add item')

        nid = self._stock.getNextId()
        item = StockItem(nid, category, item_name, item_desc, amount, item_price, self._name)
        try:
            self._shop_lock.acquire()
            r = self._stock.addStockItem(item)
            self._shop_lock.release()
            return r
        except Exception as e:
            self._shop_lock.release()
            raise e

    def remove_item(self, item_name):
        try:
            self._shop_lock.acquire()
            r = self._stock.removeStockItem(item_name)
            self._shop_lock.release()
            return r
        except Exception as e:
            self._shop_lock.release()
            raise e

    def editItem(self, itemname, new_name, item_desc, category, item_price, count):
        try:
            self._shop_lock.acquire()
            r = self._stock.editStockItem(itemname, new_name, item_desc, category, item_price, count)
            self._shop_lock.release()
            return r
        except Exception as e:
            self._shop_lock.release()
            raise e
    def getAmount(self,item_name):
        return self._stock.getAmount(item_name)
    def checkAmount(self, item_name, amount):
        amount = int(amount)
        if amount < 0:
            raise Exception("You can't remove negative amount of item")
        try:
            self._shop_lock.acquire()
            r = self._stock.checkAmount(item_name, amount)
            self._shop_lock.release()
            return r
        except Exception as e:
            self._shop_lock.release()
            raise e
    def have_rule_in_shop(self,member):
        if member.get_username() == self._founder.get_username():
            raise Exception("Assignee is already a founder of the shop!")
        if member.get_username() in self._managers:
            raise Exception("Assignee is already a manager of the shop!")
        if member.get_username() in self._owners:
            raise Exception("Assignee is already an owner of the shop!")

    def assign_owner(self, assigner_member_object, assignee_member_object):
        self.have_rule_in_shop(assignee_member_object)
        #if assigned owner was a manager need to think what to do remove from managers or... NO.. if you have a rule you cant be promoted.
        self._owners[assignee_member_object.get_username()] = assignee_member_object
        assignee_member_object.addOwnedShop(self)
        self.add_assignment(assigner_member_object, assignee_member_object, self._owners_assignments)
        return True

    def delete_owner(self, assigner_user_name, assignee_user_name):
        if assignee_user_name == self._founder.get_username():
            raise Exception("%s is Founder of the shop:%s and therefore cant be deleted from owners group" %(assignee_user_name,self._name))
        if assignee_user_name not in self._owners:
            raise Exception(assignee_user_name + " is not an owner of the shop:" + self._name)
        self.delete_assignment_owner(assigner_user_name, assignee_user_name, self._owners_assignments)
    def delete_manager(self,assigner_user_name, assignee_user_name):
        if assignee_user_name == self._founder.get_username():
            raise Exception("%s is Founder of the shop:%s and therefore cant be deleted from owners group" %(assignee_user_name,self._name))
        if assignee_user_name not in self._managers:
            raise Exception(assignee_user_name + " is not an owner of the shop:" + self._name)
        self.delete_assignment_manager(assigner_user_name, assignee_user_name, self._managers_assignments)

    def delete_assignment_owner(self, assigner_user_name, assignee_user_name, assignment):
        assignee_member_object = None
        b = False
        if assigner_user_name in assignment:
            for i in assignment[assigner_user_name]:
                if i.assignee.get_username() == assignee_user_name:
                    assignee_member_object = i.assignee
                    assignment[assigner_user_name].remove(i)
                    t.delete_assignment(i.id,self._name)
                    b = True
                    break
        if not b:
            raise Exception(assigner_user_name + " did not assignee " + assignee_user_name)
        self.recursive_delete(assignee_member_object)

    def delete_assignment_manager(self, assigner_user_name, assignee_user_name, assignment):
        assignee_member_object = None
        b = False
        if assigner_user_name in assignment:
            for i in assignment[assigner_user_name]:
                if i.assignee.get_username() == assignee_user_name:
                    assignee_member_object = i.assignee
                    assignment[assigner_user_name].remove(i)
                    t.delete_assignment(i.id,self._name)
                    b = True
                    break
        if not b:
            raise Exception(assigner_user_name + " did not assignee " + assignee_user_name)
        self.recursive_delete(assignee_member_object)

    def addTempPolicy(self, ID, name, arg1, arg2, percent):
        p = []
        for i in [ID, name, arg1, arg2, percent]:
            if i is not None:
                p.append(i)
        self._policies.append(p)
        return True

    def getTempPolicies(self):
        return self._policies

    def recursive_delete(self, member_to_delete):
        if member_to_delete.get_username() in self._owners_assignments:
            for i in self._owners_assignments[member_to_delete.get_username()]:
                self.recursive_delete(i.assignee)
                t.delete_assignment(i.id,self._name)
        if member_to_delete.get_username() in self._managers_assignments:
            for i in self._managers_assignments[member_to_delete.get_username()]:
                self.recursive_delete(i.assignee)
                t.delete_assignment(i.id,self._name)
        if member_to_delete.get_username() in self._owners_assignments:
            del self._owners_assignments[member_to_delete.get_username()]
        if member_to_delete.get_username() in self._managers_assignments:
            del self._managers_assignments[member_to_delete.get_username()]
        member_to_delete.deleteOwnedShop(self)
        member_to_delete.deleteManagedShop(self)
        if member_to_delete.get_username() in self._owners:
            del self._owners[member_to_delete.get_username()]
        if member_to_delete.get_username() in self._managers:
            del self._managers[member_to_delete.get_username()]

    def assign_manager(self, assigner_member_object, assignee_member_object):
        self.have_rule_in_shop(assignee_member_object)

        self._managers[assignee_member_object.get_username()] = assignee_member_object
        assignee_member_object.addManagedShop(self)
        self.add_assignment(assigner_member_object, assignee_member_object, self._managers_assignments)
        return True

    def get_item_id_from_name(self,item_name):
        return self._stock.get_item_id_from_name(item_name)

    def add_assignment(self, assigner_member_object, assignee_member_object, assignment):
        a= Assignment(assigner_member_object, assignee_member_object)
        if assigner_member_object.get_username() in assignment:
            assignment[assigner_member_object.get_username()].append(
                a)
        else:
            assignment[assigner_member_object.get_username()] = [
                a]
        if assignment == self._managers_assignments:
            t.add_shop_manager_assignment(self._name, a.id)
        else:
            t.add_shop_owner_assignment(self._name, a.id)


    def is_assignment(self, assigner, assignee):
        if assigner in self._owners_assignments:
            return assignee in self._owners_assignments[assigner]
        if assigner in self._managers_assignments:
            return assignee in self._managers_assignments[assigner]

    def get_founder_and_owners(self):
        all = []
        all.append(self._founder)
        for o in  self._owners.values():
            all.append(o)
        return all

    def close_shop(self):
        if self._is_open:
            self._is_open = False
            all = self.get_founder_and_owners()
            usernames = [u.get_username() for u in all]
            print(usernames)
            missed = self.notificationPlugin.alertspecificrange("The Shop \"%s\" is closed." %(self.getShopName()),usernames)
            print(missed)
            for user in all:
                if user.get_username() in missed:
                    user.addDelayedNotification("The Shop \"%s\" is closed." %(self.getShopName()))
            t.close_shop(self.getShopName())
            return True
        else:
            raise Exception('Closed shop could not be closed again!')
    def reopen_shop(self):
        if not self._is_open:
            self._is_open = True
            all = self.get_founder_and_owners()
            usernames = [u.get_username() for u in all]

            missed = self.notificationPlugin.alertspecificrange("The Shop \"%s\" is open again." % (self.getShopName()), usernames)
            for user in all:
                if user.get_username() in missed:
                    user.addDelayedNotification("The Shop \"%s\" is open again." % (self.getShopName()))
            t.reopen_shop(self.getShopName())
            return True
        else:
            raise Exception('Open shop could not be opened again!')
    # Returns whether usernae is manager
    def is_manager(self, manager_username: str) -> bool:
        return manager_username in self._managers

    def is_owner(self, owner_username: str) -> bool:
        return self._owners[owner_username] is not None or self._founder.get_username() == owner_username

    def getTotalDiscount(self, user):
        totaldiscount = 1
        for discount in self._discountPolicies:
            totaldiscount = totaldiscount * discount.getDiscount(user)
        return totaldiscount

    def getRolesInfoReport(self):
        return {'founder': self._founder.get_username(), 'managers': [m for m in self._managers],
        'owners': [m for m in self._owners]}

    def get_shop_report(self):
        return {'name': self._name, 'founder': self._founder.get_username(), 'managers': [m for m in self._managers],
                'owners': [m for m in self._owners],
                'shopopen': self.isOpen(),
                'items': self._stock.get_items_report()}

    def aqcuire_lock(self):
        '''acquires the lock of the shop'''
        self._shop_lock.acquire()

    def release_lock(self):
        '''release the lock of the shop'''
        self._shop_lock.release()

    def purchase(self, user, itemname: str, amount: int, bought_price: float):
        '''Perform purchase'''
        self._purchases_history.add(user.get_state(), itemname, amount, bought_price)
        self._stock.purchase(itemname, amount)
        all = self.get_founder_and_owners()
        usernames = [u.get_username() for u in all]
        message = "%s purchased %d of %s from shop %s" %(user.get_state(),amount,itemname,self.getShopName())
        missed = self.notificationPlugin.alertspecificrange(message, usernames)
        for user in all:
            if user.get_username() in missed:
                user.addDelayedNotification(message)
        return True

    def search(self, query: str, category: str, item_min_price: float, item_max_price: float):
        '''Performs search (non exclusive) - an item is found by query in his name/desc/category'''
        return self._stock.search(query, category, item_min_price, item_max_price)

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
    def can_add_purchase_policies(self,user):
        if user.getMember() == self._founder or user.getMember() in self._owners :
            return True
        if user.getMember() in self._managers:
            return user.getMember().can_add_purchase_policies(self.name)

    def can_add_discount_policies(self,user):
        if user.getMember() == self._founder or user.getMember() in self._owners:
            return True
        if user.getMember() in self._managers:
            return user.getMember().can_add_discount_policies(self.name)

    def addPurchasePolicy(self, policy):
        self._purchaseLock.acquire()
        self._purchasePolicies.append(policy)
        t.add_shop_policy(policy,self._name,"purchase",1)
        self._purchaseLock.release()
        return True

    def addDiscountPolicy(self, policy):
        self._discountLock.acquire()
        self._discountPolicies.append(policy)
        t.add_shop_policy(policy, self._name, "discount", 1)
        self._discountLock.release()
        return True

    def remove_policy(self, ID, type1):
        done = False
        if type1 == "discount":
            self._discountLock.acquire()
            for d in self._discountPolicies:
                if d.getID() == ID:
                    self._discountPolicies.remove(d)
                    t.delete_shop_policy(ID,self._name,"discount")
                    done = True
            self._discountLock.release()
        else:
            self._purchaseLock.acquire()
            for d in self._purchasePolicies:
                if d.getID() == ID:
                    self._purchasePolicies.remove(d)
                    t.delete_shop_policy(ID, self._name, "purchase")
                    done = True
            self._purchaseLock.release()
        print(done,ID,type1)
        return done

    def getItemPrice(self, name):
        return self._stock.getItem(name).getPrice()

    def getPolicies(self):
        ret = []
        for p in self._discountPolicies:
            ret.append(["discount", p.getID(), p.getDiscount()])
        for p in self._purchasePolicies:
            ret.append(["purchase", p.getID()])
        return ret

    def validate_purchase(self, user, name):
        item = self._stock.getItem(name)
        for policy in self._purchasePolicies:
            if not policy.apply(user, item):
                return False
        return True

    def calculate_price(self, user, name, amount):
        item = self._stock.getItem(name)
        disc = self.findDiscount(user, item)
        # print(name, disc,item.getPrice()*amount*disc)
        return round(item.getPrice() * amount * disc, 3)

    def calculate_price_for_general_item(self, user, itemname):
        item = self._stock.getItem(itemname)
        disc = self.findDiscount(user, item)
        # print(name, disc,item.getPrice()*amount*disc)
        return round(item.getPrice() * disc, 3)

    def findDiscount(self, user, item):
        disc = 1
        for policy in self._discountPolicies:
            # print(policy,policy.apply(user, item))
            if policy.apply(user, item):
                d = policy.getDiscount()
                disc *= (1 - d / 100)
        return disc
    def get_permission_report(self,member_name):
        m = self._managers[member_name]
        p = m.get_permissions(self._name)
        ret = p.get_permission_report_json()
        return ret

    def getCategories(self):
        return self._stock.getCategories()