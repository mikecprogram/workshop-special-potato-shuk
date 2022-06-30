
import threading
import sys

from Dev.DomainLayer.Objects.Policies.policyIsAge import policyIsAge
from Dev.DomainLayer.Objects.Policies.policyIsMember import policyIsMember
from Dev.Mock_init import Mock
from Dev.DAL.objects.DBInit import initializeDatabase

# from Logger import Logger
from Dev.DomainLayer.Objects.InitFileLoader import init_file_loader
from Dev.DomainLayer.Objects.Policies.policyAnd import policyAnd
from Dev.DomainLayer.Objects.Policies.policyMax import policyMax
from Dev.DomainLayer.Objects.Policies.policyAdd import policyAdd
from Dev.DomainLayer.Objects.Policies.policyIf import policyIf
from Dev.DomainLayer.Objects.Policies.policyIsAfterTime import policyIsAfterTime
from Dev.DomainLayer.Objects.Policies.policyIsFounder import policyIsFounder
from Dev.DomainLayer.Objects.Policies.policyIsOwner import policyIsOwner
from Dev.DomainLayer.Objects.Policies.policyXor import policyXor
from Dev.DomainLayer.Objects.Policies.policyIsCategory import policyIsCategory
from Dev.DomainLayer.Objects.Policies.policyIsItem import policyIsItem
from Dev.DomainLayer.Objects.Policies.policyIsShop import policyIsShop
from Dev.DomainLayer.Objects.Policies.policyNot import policyNot
from Dev.DomainLayer.Objects.Policies.policyOr import policyOr
from Dev.DomainLayer.Objects.Policies.policyHasAmount import policyHasAmount
from Dev.DomainLayer.Objects.Policies.policyHasPrice import policyHasPrice
from Dev.DomainLayer.Objects.Shop import Shop
from Dev.DomainLayer.Objects.User import User
from Dev.DomainLayer.Objects.ExternalServices import ExternalServices

from Dev.DomainLayer.Objects.Member import Member
from Dev.DomainLayer.Objects.Security import Security
from Dev.DomainLayer.Objects.paymentServiceInterface import paymentServiceInterface
from Dev.DomainLayer.Objects.shippingServiceInterface import shippingServiceInterface

from Dev.DomainLayer.Objects.db_dict import TransformedDictMember,TransformedDictShop
from Dev.DAL.Transactions import t



prem = [
    "premission1",
    "premission2",
    "premission3",
    "premission4",
    "premission5",
    "premission6",
    "premission7",
    "premission8",
    "premission9",
    "premission10",
    "premission11",
    "premission12",
    "premission13",
]

simplePolicies = [
    "isItem", "isCategory", "isShop", "hasAmount", "hasPrice", "hasAmount", "hasPrice","isMember","isFounder","isAge","isAfterTime", "isOwner"
]

compositePolicies = [
    "not", "and", "or", "xor", "max", "add", "if"
]


def is_valid_password(password):
    if len(password) >= 8:  # need to add constraints on pass TODO
        return True
    else:
        raise Exception("invalid password")  # may add some hint about a valid password TODO


debug = True

notyplugin = None
class dummyNotify():
    def alertspecificrange(self, message, ran):
        return ran
    def alert(self, message):
        pass
class Market():

    def __init__(self, notificationPlugin):
        if not Mock:
            initializeDatabase()
        if notificationPlugin is None:
            self._notificationPlugin = dummyNotify()
        else:
            self._notificationPlugin = notificationPlugin
        if not Mock:
            self._members = TransformedDictMember()
            self._shops = TransformedDictShop()
            self._shops.set_notiplugin(self._notificationPlugin)
        else:
            self._members = {}
            self._shops = {}
        self._membersLock = threading.Lock()
        self._onlineVisitors = {}  # {token, User}
        self._nextToken = -1
        self._enterLock = threading.Lock()
        self._nextPolicy = 1
        self._policyLock = threading.Lock()
        self._nextBid = 1
        self._bidLock = threading.Lock()
        self._security = Security()
        #loadConfigFile:
        self.init_file_loader = init_file_loader()
        self.load_sys_admin()
        #self.loadcondig()
        self.reloadExternalServices()

    def load_sys_admin(self):
        sys_username,sys_password = self.init_file_loader.getManagerDetailsa(-1)
        if sys_username not in self._members:
            hashedPassword = self._security.hash(sys_password)
            sysmanager = Member(sys_username,hashedPassword,self)# this is sys manager.
            self._members[sys_username] = sysmanager

    def loadcondig(self):
        for hhhhh in range(2,4):
            u, p = self.init_file_loader.getManagerDetailsa(hhhhh)
            print(u)
            print(p)
            if u not in self._members:
                hashedPassword = self._security.hash(p)
                mem = Member(u,hashedPassword)
                self._members[u] = mem
        u3, p3 = self.init_file_loader.getManagerDetailsa(3)
        u, p = self.init_file_loader.getManagerDetailsa(2)
        t2 = self.enter()
        """self.login(t2,u,p)
        self.shop_open(t2,"s")
        self.adding_item_to_the_shops_stock(t2,"Bamba","s","Snacks","Tasty",30.0,20)
        self.shop_manager_assignment(t2,"s",u3)
        self.grant_permission(1,"s",t2,u3)
        self.exit(t2)
        print("DONEDONEDONEDONEDONEDONEDONEDONE")"""
    def resetSystem(self):
        #todo DROP TABLE
        #todo START TABLE
        self.init_file_loader.load_config_file()
        self.load_sys_admin()

        #todo add him to system
        self.reloadExternalServices()
    def reloadExternalServices(self):
        external_payment_service = paymentServiceInterface(self.init_file_loader.url)
        external_supplement_service = shippingServiceInterface(self.init_file_loader.url)
        self._externalServices = ExternalServices(external_payment_service, external_supplement_service)

    def isToken(self, token):
        if (not (token in self._onlineVisitors)):
            raise Exception("The token was not found")
        return True

    # sync me on [enter]
    def enter(self):
        # return token id
        # save token id with a user-guest attached
        self._enterLock.acquire()
        currentToken = self._nextToken
        self._nextToken = self._nextToken + 1
        self._enterLock.release()
        self._onlineVisitors[currentToken] = User(self)
        return currentToken

    def get_user_state(self, token):
        if self.isToken(token):
            return self._onlineVisitors[token].get_state()

    def exit(self, token):
        if self.isToken(token):
            self._onlineVisitors[token].exit()
            del self._onlineVisitors[token]
            return True
        return False

    def register(self, token, username, password):
        if self.isToken(token):
            user = self.getUser(token)
            if user.isMember():
                raise Exception("Logged in member can't register for some reason")
            username = username.strip()
            if not self.is_member(username):
                if is_valid_password(password):
                    if username != "":
                        hashedPassword = self._security.hash(password)
                        member = Member(username, hashedPassword)
                        self._members[username] = member
                        return True
                    else:
                        raise Exception('Username can not be null')
            else:
                raise Exception('Username is taken!')

    def is_member(self, username):
        return username in self._members.keys()

    def is_logged_in(self, token):
        u = self._onlineVisitors.get(token)
        if u is not None:
            if u.isMember():
                return True
        raise Exception('Only logged in members can open this page.')

    def get_age(self, token):
        if self.isToken(token):
            user = self.getUser(token)
            if self.isMember():
                return user.getAge()
            else:
                raise Exception("This user is not a member")

    def set_age(self, token, age):
        if self.isToken(token):
            user = self.getUser(token)
            if self.isMember():
                return user.setAge(age)

    def calculate_cart_price(self, token):
        try:
            if self.isToken(token):
                user = self.getUser(token)
                return user.calculate_cart_price()
        except Exception as e:
            return -1
    def shipping_request(self, token, items):
        if self.isToken(token):
            pass

    def logout(self, token):
        if self.isToken(token):
            user = self.getUser(token)
            user.logout()

    def is_logged_in_by_username(self,username):
        for un in self._onlineVisitors.values():
            if un.get_state() == username:
                return True
        return False

    def login(self, token, username, password):
        if self.isToken(token):
            if self.is_logged_in_by_username(username):
                raise Exception("The user %s is already logged in." % username)
            if not (is_valid_password(password)):
                raise Exception("Password is not valid")
            if username in self._members:
                member = self._members[username]
                hashed = self._security.hash(password)
                if member.isHashedCorrect(hashed):
                    user = self.getUser(token)
                    self._onlineVisitors[token] = user
                    return user.login(member)
                else:
                    raise Exception("Wrong password")
            else:
                raise Exception("No user such as %s" % username)

    def info_about_shop_in_the_market_and_his_items_name(self, token, shop_name):
        if self.isToken(token):
            if self.is_shop(shop_name):
                return self._shops[shop_name].get_shop_report()
            else:
                raise Exception('Shop does not exist with the given shop name!')

    def general_items_searching(self, token, query, category=None, item_minPrice=-1, item_maxPrice=-1):
        if query is None:
            query = ""
        query = query.strip()
        if not (category is None):
            category = category.strip()
        ret = {}
        if self.isToken(token):
            for shop in self._shops.values():
                answers = shop.search(query, category, item_minPrice, item_maxPrice)
                if answers is not None:
                    ret[shop.getShopName()] = answers
            return ret

    def info_about_item_in_shop(self, token, itemname, shop_name):
        if self.isToken(token) and shop_name in self._shops.keys():
            return self._shops[shop_name].getItemInfo(itemname)
        raise Exception("No such shop %s" % shop_name)

    def addToCart(self, token, itemid, shop_name, amount):
        if self.isToken(token):
            user = self.getUser(token)
            if shop_name in self._shops.keys():
                shop = self._shops[shop_name]
                user.addToCart(itemid, shop, amount);
                pass
            raise Exception("No such shop %s" % shop_name)

    def getCartContents(self, token):
        if self.isToken(token):
            user = self.getUser(token)
            return user.checkBaskets()

    def removeFromCart(self, token, item_name, shop_name, amount):
        if self.isToken(token):
            user = self.getUser(token)
            return user.removeFromCart(item_name, shop_name, amount)


    def add_policy(self, token, shopname, percent, name, arg1=None, arg2=None):
        if self.isToken(token):
            if percent < 0:
                raise Exception('Discount can\'t be negative..')
            shop = self.get_shop_by_name(shopname)
            if shop is None:
                raise Exception('No shop named '+shopname)
            if name in simplePolicies:
                self._policyLock.acquire()
                ID = self._nextPolicy
                self._nextPolicy += 1
                self._policyLock.release()
                return shop.addTempPolicy(ID, name, arg1, arg2, percent)
            raise Exception('Cannot add policy!')

    def get_my_policies(self, token, shopname):
        self.isToken(token)
        shop = self.get_shop_by_name(shopname)
        if shop is None:
            raise Exception('No shop named ' + shopname)
        return shop.getTempPolicies()

    def get_shop_policies(self, token, shopname):
        if not self.isToken(token):
            raise Exception('Bad token!')
        for n, s in self._shops.items():
            if n == shopname:
                return s.getPolicies()

    def add_discount_policy_to_shop(self, token, shopname, policyID):
        self.isToken(token)
        user = self.getUser(token)
        shop = self.get_shop_by_name(shopname)
        if shop.can_add_discount_policies(user):
            policy = self.makePolicy(shop, policyID)
            return shop.addDiscountPolicy(policy)
        raise Exception("You do not have permission to add discount policy")

    def add_purchase_policy_to_shop(self, token, shopname, policyID):
        if not self.isToken(token):
            raise Exception('Bad token!')
        user = self.getUser(token)
        shop = self.get_shop_by_name(shopname)
        if shop.can_add_purchase_policies(user):
            policy = self.makePolicy(shop, policyID)
            return shop.addPurchasePolicy(policy)
        else:
            raise Exception("You do not have permission to add purchase policy")

    def makePolicy(self, shop, PID):
        pols = shop.getTempPolicies()
        pol = None
        for p in pols:
            if p[0] == PID:
                pol = p
                break
        if pol is None:
            raise Exception("bad policy ID!")
        if pol[1] in simplePolicies:
            if pol[1] == "isShop":
                return policyIsShop(p[0], p[2])
            if pol[1] == "isFounder":
                return policyIsFounder(p[0], p[2])
            if pol[1] == "isMember":
                return policyIsMember(p[0], p[2])
            if pol[1] == "isOwner":
                return policyIsOwner(p[0], p[2])
            if pol[1] == "isCategory":
                return policyIsCategory(p[0], p[3], p[2])
            if pol[1] == "isItem":
                return policyIsItem(p[0], p[3], p[2])
            if pol[1] == "hasAmount":
                return policyHasAmount(p[0], p[4], p[2], p[3])
            if pol[1] == "isAge":
                return policyIsAge(p[0], p[3], p[2])
            if pol[1] == "hasPrice":
                return policyHasPrice(p[0], p[4], p[2], p[3])
            if pol[1] == "isAfterTime":
                return policyIsAfterTime(p[0], p[4], p[2], p[3])
        else:
            if pol[1] == "not":
                pt = self.makePolicy(shop, p[2])
                return policyNot(p[0], pt)
            if pol[1] == "and":
                pt1 = self.makePolicy(shop, p[2])
                pt2 = self.makePolicy(shop, p[3])
                return policyAnd(p[0], pt1, pt2)
            if pol[1] == "or":
                pt1 = self.makePolicy(shop, p[2])
                pt2 = self.makePolicy(shop, p[3])
                return policyOr(p[0], pt1, pt2)
            if pol[1] == "xor":
                pt1 = self.makePolicy(shop, p[2])
                pt2 = self.makePolicy(shop, p[3])
                return policyXor(p[0], pt1, pt2)
            if pol[1] == "if":
                pt1 = self.makePolicy(shop, p[2])
                pt2 = self.makePolicy(shop, p[3])
                return policyIf(p[0], pt1, pt2)
            if pol[1] == "add":
                pt1 = self.makePolicy(shop, p[2])
                pt2 = self.makePolicy(shop, p[3])
                return policyAdd(p[0], pt1, pt2)
            if pol[1] == "max":
                pt1 = self.makePolicy(shop, p[2])
                pt2 = self.makePolicy(shop, p[3])
                return policyMax(p[0], pt1, pt2)

    def compose_policy(self, token, shopname, name, arg1, arg2):
        if not self.isToken(token):
            raise Exception('Bad token!')
        ok = False
        shop = self.get_shop_by_name(shopname)
        if shop is None:
            raise Exception('No shop named ' + shopname)
        if name in compositePolicies:

            PIDS = [p[0] for p in shop.getTempPolicies()]
            if arg1 in PIDS and (arg2 is None or arg2 in PIDS):
                ok = True
        if ok:
            self._policyLock.acquire()
            ID = self._nextPolicy
            self._nextPolicy += 1
            self._policyLock.release()
            return shop.addTempPolicy(ID, name, arg1, arg2, None)
        raise Exception('Cannot add policy!')

    def remove_policy_from_shop(self, token, shopname, policyID,type1):
        if not self.isToken(token):
            raise Exception('Bad token!')
        s = self._shops[shopname]
        return s.remove_policy(policyID,type1)

    def calculate_item_price(self, token, shopname, itemname):
        try:
            self.isToken(token)
            user = self.getUser(token)
            shop = self.get_shop_by_name(shopname)
            return user.calculate_item_price(shop,itemname)
        except Exception as e:
            return -1
        return -1

    def Shopping_cart_purchase(self, token, card_number, month, year, holder, ccv, id, name, address, city, country, zip):
        if self.isToken(token):
            user = self.getUser(token)
            if not user.validate_cart_purchase():
                raise Exception('Cart did not pass purchase policy!')
            price = user.calculate_cart_price()
            # where do i use the price???
            tid = self._externalServices.execute_payment(card_number, month, year, holder, ccv, id)
            if tid < 0:
                raise Exception('Payment failed!')
            try:
                if user.purchase():
                    if self._externalServices.execute_shipment(name, address, city, country, zip) > 0:
                        return True
                    raise Exception('Shipment failed!')
                raise Exception('failed to remove items from shop during purchase!')
            except Exception as e:
                self._externalServices.cancel_payment(tid)
                raise e

    def bid_shop_item(self, token, shopname, itemname, amount, bidPrice):
        self.isToken(token)
        shop = self.get_shop_by_name(shopname)
        user = self.getUser(token).getUsername()
        self._bidLock.acquire()
        bidId = self._nextBid
        self._nextBid += 1
        self._bidLock.release()
        shop.add_bid(bidId, user, itemname, amount, bidPrice)
        return True

    def getBids(self, token, shopname):
        self.isToken(token)
        shop = self.get_shop_by_name(shopname)
        return shop.getBids()

    def acceptBid(self, token, shopname, bidId, counter):
        self.isToken(token)
        member = self.getUser(token).getMember()
        shop = self.get_shop_by_name(shopname)
        return shop.acceptBid(bidId, member, counter)

    def rejectBid(self, token, shopname, bidId):
        self.isToken(token)
        member = self.getUser(token).getMember()
        shop = self.get_shop_by_name(shopname)
        shop.rejectBid(bidId, member)
    
    def payBid(self, token, bidId, card_number, month, year, holder, ccv, id, name, address, city, country, zip):
        self.isToken(token)
        user = self.getUser(token)
        if bidId not in user.getMember().acceptedBids.keys():
            raise Exception('this bid id is either pending or broken!')
        bid = user.getMember().acceptedBids[bidId]
        shop = self.get_shop_by_name(bid[0])
        itemname = bid[2]
        amount = bid[3]
        price = bid[4]
        count = shop.getAmount(itemname)

        tid = self._externalServices.execute_payment(card_number, month, year, holder, ccv, id)
        if tid < 0:
            raise Exception('Payment failed!')
        try:
            if shop.editItem(itemname, None, None, None, None, count-amount):
                if self._externalServices.execute_shipment(name, address, city, country, zip) > 0:
                    user.getMember().acceptedBids.pop(bidId)
                    shop.bids.pop(bidId)
                    shop.bidAccepts.pop(bidId)
                    t.delete_bid(bidId)
                    shop.notify_all_owners_and_founder("The bid %d was purchase successfully" % bidId)
                    return True
                raise Exception('Shipment failed!')
            raise Exception('failed to remove items from shop during purchase!')
        except Exception as e:
            self._externalServices.cancel_payment(tid)
            raise e

    def get_inshop_purchases_history(self, token, shopname):
        if self.isToken(token):
            if shopname in self._shops:
                if self.getUser(token).is_admin():
                    sh = self.get_shop_by_name(shopname)
                    return sh.get_inshop_purchases_history()
                else:
                    return self._onlineVisitors[token].get_inshop_purchases_history(shopname)
            else:
                raise Exception('Shop not found with given name!')
        else:
            raise Exception('Timed out token!')

    def getUser(self, token):
        return self._onlineVisitors[token]
    def isOnline(self,username):
        for i in self._onlineVisitors.keys():
            if self._onlineVisitors[i].get_state() == username:
                return i
        return None
    """
    In order to check if user is still connected we use  self.isToken(token)
    To get user we use self._onlineVisitors[token]
    To check if user is member we use user.isMember():
    If we succed we return True
    Else we throw Exception (Or, in rare occasion we return False)
    """

    def shop_open(self, token, shop_name):
        if self.isToken(token):
            shop_name = str(shop_name).strip()
            if shop_name == "":
                raise Exception("Shop name can't be null")
            if not shop_name in self._shops:
                user = self.getUser(token)
                newShop = Shop(shop_name, user.getMember(), self._notificationPlugin)
                self._shops[shop_name] = newShop
                user.getMember().openShop(newShop)
                return True
            else:
                raise Exception("There is already a shop with given name in the market, try another name please!")

    def shop_reopen(self, token, shop_name):
        if self.isToken(token):
            shop_name = str(shop_name).strip()
            if shop_name == "":
                raise Exception("Shop name can't be null")
            if shop_name in self._shops:
                user = self.getUser(token)
                user.getMember().reopen_shop(shop_name)
                return True
            else:
                raise Exception("There is no such shop in market")

    def adding_item_to_the_shops_stock(self, token, item_name, shop_name, category, item_desc, item_price, amount):
        if self.isToken(token) and self.is_logged_in(token):
            u = self.getUser(token)
            if shop_name in self._shops.keys():
                s = self._shops[shop_name]
                return s.add_item(u.getUsername(), item_name, category, item_desc, item_price, amount)
            raise Exception('Bad shop name!')
        raise Exception('Bad token!')

    def get_shop_by_name(self,shopname):
        if shopname in self._shops.keys():
            return self._shops[shopname]
        raise Exception('No such shop as %s' % shopname)

    def deleting_item_from_shop_stock(self, token, item_name, shop_name):
        if self.isToken(token):
            s = self.get_shop_by_name(shop_name)
            r = s.remove_item(item_name)
            return r

    def validate_purchase_policy(self, token):
        if not self.isToken(token):
            raise Exception('Bad token!')
        user = self.getUser(token)
        return user.validate_cart_purchase()

    def change_items_details_in_shops_stock(self, token, itemname, shop_name, new_name, item_desc, category,
                                            item_price, amount):
        if self.isToken(token):
            if shop_name in self._shops.keys():
                s = self._shops[shop_name]
                return s.editItem(itemname, new_name, item_desc, category,
                                  item_price, amount)
        raise Exception('No such shop as %s' % shop_name)

    def shopping_carts_add_item(self, token, item_name, shop_name, amount):
        if self.isToken(token):
            if shop_name in self._shops.keys():
                s = self._shops[shop_name]
                valid = s.checkAmount(item_name, amount)
                if valid:
                    self._onlineVisitors[token].addToCart(s, item_name, amount)
                    return True
                else:
                    raise Exception('Amount does not suffice for you')
            else:
                raise Exception('No such shop as %s' % shop_name)
        raise Exception('Bad token!')

    def shop_owner_assignment(self, token, shop_name, member_name_to_assignUserName):
        if self.isToken(token):
            if self.is_member(member_name_to_assignUserName):
                self._onlineVisitors[token].assign_owner(shop_name, self._members[member_name_to_assignUserName])
                return True
            else:
                raise Exception('member does not exist to be assigned!')

    def shop_manager_assignment(self, token, shop_name, member_name_to_assignUserName):
        if self.isToken(token):
            if self.is_member(member_name_to_assignUserName):
                self._onlineVisitors[token].assign_manager(shop_name, self._members[member_name_to_assignUserName])
                return True
            else:
                raise Exception('member does not exist to be assigned!')

    def shop_closing(self, token, shop_name):
        if self.isToken(token):
            if self.is_shop(shop_name):
                return self._onlineVisitors[token].close_shop(shop_name)
            else:
                raise Exception('Shop does not exist with the given shop name!')



    def shop_manager_permission_adding(self, token, manager_name_to_update, permission_code, shop_name):
        if self.isToken(token):
            if shop_name not in self._shops:
                raise Exception('Shop does not exist with the given shop name!')
            self._onlineVisitors[token].grant_permission(permission_code, shop_name, manager_name_to_update)
        return "Permission with code: " + permission_code + " has been added to manager: "+manager_name_to_update +" of shop: "+ shop_name +" successfully!"

    def shop_manager_permission_removing(self, token, manager_name_to_update, permission_code, shop_name):
        if self.isToken(token):
            if shop_name not in self._shops:
                raise Exception('Shop does not exist with the given shop name!')
            self._onlineVisitors[token].withdraw_permission(permission_code, shop_name, manager_name_to_update)
        return "Permission with code: " + permission_code + " has been removed from manager: "+manager_name_to_update +" of shop: "+ shop_name +" successfully!"


    def shops_roles_info_request(self, token,shopName):
        if self.isToken(token):
            return self._onlineVisitors[token].getRolesInfoReport(shopName)

    def shop_manager_permissions_check(self, token:int,shop_name:str,manager_name:str):
        if self.isToken(token):
            return self._onlineVisitors[token].get_permissions_report(shop_name, manager_name)


    def is_shop(self, shopName):
        if shopName in self._shops:
            return True
        else:
            raise Exception("Shop does not exist with the given shop name!")

    def grant_permission(self, permission_code, shop_name, token, target_manager):
        if self.isToken(token):
            if self.is_shop(shop_name):
                self._onlineVisitors[token].grant_permission(permission_code, shop_name, target_manager)
                return True
            else:
                raise Exception('Shop does not exist with the given shop name!')
        else:
            raise Exception('Timed out token!')

    def withdraw_permission(self, permission_code, shop_name, token, target_manager):
        if self.isToken(token):
            if self.is_shop(shop_name):
                self._onlineVisitors[token].withdraw_permission(permission_code, shop_name, target_manager)
                return True
            else:
                raise Exception('Shop does not exist with the given shop name!')
        else:
            raise Exception('Timed out token!')

    def archive_purchase(self, token):
        if self.isToken(token):
            self._onlineVisitors[token].archive_purchase_cart(token)
        return True

    def get_all_members_name(self, token):  # WTF does this func do?? why does it do it that way??
        if self.isToken(token) and self.is_logged_in(token):
            if self.getUser(token).is_admin():
                self._enterLock.acquire()
                online_members = list(self._onlineVisitors.values())
                online_members = [u.getUsername() for u in online_members if u.isMember()]
                self._membersLock.acquire()
                self._enterLock.release()
                offline_members = list(self._members.keys())
                self._membersLock.release()
                offline_members = [mn for mn in offline_members if mn not in online_members]
                return [online_members, offline_members]
            else:
                raise Exception('Not Admin!')
        else:
            raise Exception('Timed out token!')

    def get_member_info(self, token, member_name):
        if self.isToken(token) and self.is_logged_in(token):
            if self.getUser(token).is_admin():
                if self.is_member(member_name):
                    self._membersLock.acquire()
                    m = self._members[member_name]
                    output = m.get_member_info()
                    self._membersLock.release()
                    return output
                else:
                    raise Exception(member_name + " is not Member")
            else:
                raise Exception('Not Admin!')

    def delete_shop_owner(self, token: int, shop_name: str, owner_name: str):
        if self.isToken(token) and self.is_logged_in(token):
            self._membersLock.acquire()
            member = self._members[self.getUser(token).getUsername()]
            if self.is_member(owner_name):
                try:
                    member.delete_shop_owner(shop_name, owner_name)
                    self._membersLock.release()
                except Exception as e:
                    self._membersLock.release()
                    raise e
            else:
                self._membersLock.release()
                raise Exception(owner_name + " is not Member")

    def delete_shop_manager(self, token: int, shop_name: str, manager_name: str):
        if self.isToken(token) and self.is_logged_in(token):
            self._membersLock.acquire()
            member = self._members[self.getUser(token).getUsername()]
            if self.is_member(manager_name):
                try:
                    member.delete_shop_manager(shop_name, manager_name)
                    self._membersLock.release()
                except Exception as e:
                    self._membersLock.release()
                    raise e
            else:
                self._membersLock.release()
                raise Exception(manager_name + " is not Member")

    def delete_member(self, token: int, member_name: str):
        try:
            self._enterLock.acquire()
            self._membersLock.acquire()
            if self.isToken(token) and self.is_logged_in(token):
                if self.getUser(token).is_admin():
                    if self.is_member(member_name):
                        m = self._members[member_name]
                        if m.does_have_role():
                            raise Exception(member_name + " have roles!")
                        else:
                            online_members = list(self._onlineVisitors.values())
                            online_members = [u for u in online_members if u.isMember() and u.getUsername() == member_name]
                            if len(online_members) == 1:
                                online_members[0].logout()
                            del self._members[member_name]
                    else:
                        raise Exception(member_name + " is not Member")
                else:
                    raise Exception('You are not an Admin.')

            self._membersLock.release()
            self._enterLock.release()
        except Exception as e:
            self._membersLock.release()
            self._enterLock.release()
            raise e

    def get_founded_shops(self, token):
        if self.isToken(token):
            if self.is_logged_in(token):
                try:
                    self._enterLock.acquire()
                    output = self.getUser(token).getMember().get_founder_shops()
                    self._enterLock.release()
                    return output
                except Exception as e:
                    self._enterLock.release()

    def get_managed_shops(self, token):
        if self.isToken(token):
            if self.is_logged_in(token):
                self._enterLock.acquire()
                output = self.getUser(token).getMember().get_manage_shops()
                self._enterLock.release()
                return output

    def get_owned_shops(self, token):
        if self.isToken(token):
            if self.is_logged_in(token):
                self._enterLock.acquire()
                output = self.getUser(token).getMember().get_owner_shops()
                self._enterLock.release()
                return output

    def get_eligible_members_for_shop(self, token: int, shop_name: str):
        if self.isToken(token):
            self._membersLock.acquire()
            output = [m.get_username() for m in self._members.values() if m.is_eligible_members(shop_name)]
            self._membersLock.release()
            return output
        else:
            raise Exception('Timed out token!')

    def get_all_categories(self):
        return {shop.getShopName(): shop.getCategories() for shop in self._shops.values()}

