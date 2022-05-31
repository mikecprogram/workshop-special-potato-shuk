from operator import is_
import time
import threading
import sys

# from Logger import Logger
from Dev.DomainLayer.Objects.Shop import Shop
from Dev.DomainLayer.Objects.User import User
from Dev.DomainLayer.Objects.ExternalServices import ExternalServices

from Dev.DomainLayer.Objects.Member import Member
from Dev.DomainLayer.Objects.Security import Security
prem=[
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

def is_valid_password(password):
    if len(password) >= 8:  # need to add constraints on pass TODO
        return True
    else:
        raise Exception("invalid password")  # may add some hint about a valid password TODO


debug = False
maxtimeonline = 1  # 60 * 10  # 10 minutes


class Market():

    def prid(self, txt):
        if debug:
            print(txt)

    def __init__(self, external_payment_service, external_supplement_service, system_admin_name, password,
                 maxtimeonline=60 * 10):  # 10 minutes
        self._maxtimeonline = maxtimeonline
        self._members = {}
        self._onlineVisitors = {}  # {token, User}
        self._onlineDate = {}  # hashmap  used only by isToken,enter
        self._nextToken = -1
        self._enterLock = threading.Lock()
        self._shops = {}  # {shopName, shop}
        self._security = Security()
        self._externalServices = ExternalServices(external_payment_service,external_supplement_service)

    # returns boolean, returns if current date < 10Minutes+_onlineDate[token]
    # if #t update _onlineDate[token]
    # this will be checked before each user function
    # this function returns whether the token is valid
    def isToken(self, token):
        if (not (token in self._onlineVisitors)):
            self.prid("The token was not found")
            return False
        currentTime = time.time()
        if (currentTime - self._onlineDate[token] < self._maxtimeonline):
            self._onlineDate[token] = currentTime
            return True
        self.prid("Session time out for token %d" % token)
        return False

    # sync me on [enter]
    def enter(self):
        # return token id
        # save token id with a user-guest attached
        self._enterLock.acquire()
        currentToken = self._nextToken
        self._nextToken = self._nextToken + 1
        self._enterLock.release()
        currentToken = self._nextToken
        self._onlineVisitors[currentToken] = User(self)
        self._onlineDate[currentToken] = time.time()
        return currentToken

    def exit(self, token):
        if self.isToken(token):
            self._onlineVisitors[token].exit()
            del self._onlineVisitors[token]
            del self._onlineDate[token]
            return True
        return False

    def register(self, token, username, password):
        if self.isToken(token):
            user = self.getUser(token)
            if user.isMember():
                raise Exception("Logged in member can't register for some reason")
            if not self.is_member(username):
                if is_valid_password(password) and username!="":
                    hashedPassword = self._security.hash(password)
                    member = Member(username, hashedPassword)
                    self._members[username] = member
                    return True
                else:
                    raise Exception('invalid password!')
            else:
                raise Exception('Username is taken!')
        else:
            return False

    def is_member(self, username):
        return username in self._members.keys()

    def is_active(self, token):
        return self._onlineVisitors.get(token) is not None

    def is_logged_in(self, token):
        u=self._onlineVisitors.get(token)
        if u is not None:
            return u.isMember()

    def shipping_request(self, token, items):
        if self.isToken(token):
            pass

    def logout(self, token):
        if self.isToken(token):
            user = self.getUser(token)
            user.logout()

    def login(self, token, username, password):
        if self.isToken(token):
            if not (is_valid_password(password)):
                raise Exception("Password is not valid")
            if username in self._members:
                member = self._members[username]
                hashed = self._security.hash(password)
                if member.isHashedCorrect(hashed):
                    user = self.getUser(token)
                    user.login(member)
                    return True
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

    def general_items_searching(self, token, item_name, category, item_keyword, item_maxPrice):
        ret=[]
        if self.isToken(token):
            for n,s in self._shops.items():
                #print(n)
                l=s.search( item_name, category, item_keyword, item_maxPrice)
                if not l is None:
                    for i in l:
                        ret.append(i)
                #print("ret len after "+n+": "+str(ret))
        return ret

    def info_about_item_in_shop(self, token, itemname, shop_name):
        if self.isToken(token) and shop_name in self._shops.keys():
            return self._shops[shop_name].getItemInfo(itemname)

    def addToCart(self, token, itemid, shop_name, amount):
        if self.isToken(token):
            user = self.getUser(token)
            shop = self._shops[shop_name]
            user.addToCart(itemid, shop, amount);
            pass

    def getCartContents(self, token):
        if self.isToken(token):
            user = self.getUser(token)
            return user.checkBaskets();

    def removeFromCart(self, token, itemid, shop_name, amount):
        if self.isToken(token):
            user = self.getUser(token)
            user.removeFromCart(itemid,shop_name, amount);
            pass

    def Shopping_cart_purchase(self, token):
        if self.isToken(token):
            user = self.getUser(token)
            #here call function to validate purchase, ckeck payment and delivery.
            #if any check fails we raise exception and dont get to the line: user.purchase()
            return user.purchase()

    def get_inshop_purchases_history(self, token, shopname):
        if self.isToken(token):
            if shopname in self._shops:
                self._onlineVisitors[token].get_inshop_purchases_history(shopname)
            else:
                raise Exception('Shop not found with given name!')
        else:
            raise Exception('Timed out token!')
    def getUser(self,token):
        return self._onlineVisitors[token]

    """
    In order to check if user is still connected we use  self.isToken(token)
    To get user we use self._onlineVisitors[token]
    To check if user is member we use user.isMember():
    If we succed we return True
    Else we throw Exception (Or, in rare occasion we return False)
    """

    def shop_open(self, token, shop_name):
        if self.isToken(token):
            if not shop_name in self._shops:
                if shop_name=="":
                    raise Exception("bad shop name")
                user = self.getUser(token)
                newShop = Shop(shop_name, user.getMember())
                self._shops[shop_name] = newShop
                user.getMember().openShop(newShop)
                return True
            else:
                raise Exception("There is already a shop with given name in the market, try another name please!")

    def adding_item_to_the_shops_stock(self, token, item_name, shop_name, category, item_desc, item_price, amount):
        if self.isToken(token) and self.is_logged_in(token):
            u=self.getUser(token)
            if shop_name in self._shops.keys():
                s=self._shops[shop_name]
                return s.add_item(u.getUsername(), item_name, category, item_desc, item_price, amount)
        raise Exception('Bad token!')

    def deleting_item_from_shop_stock(self, token, item_name, shop_name, amount):
        if self.isToken(token):
            
            if shop_name in self._shops.keys():
                s=self._shops[shop_name]
                
                r = s.remove_item(item_name, amount)
                return r
        raise Exception('Bad token!')

    def change_items_details_in_shops_stock(self, token, itemname,  shop_name, new_name, item_desc, item_price):
        if self.isToken(token):
            if shop_name in self._shops.keys():
                s = self._shops[shop_name]
                return s.editItem(itemname, new_name, item_desc, item_price)
        raise Exception('Bad token!')

    def shopping_carts_add_item(self, token, item_name, shop_name, amount):
        if self.isToken(token):
            if shop_name in self._shops.keys():
                s = self._shops[shop_name]
                valid = s.checkAmount(item_name, amount)
                if valid:
                    self._onlineVisitors[token].addToCart(s, item_name, amount)
                    return True
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
                return self._onlineVisitors[token].close_shop()
            else:
                raise Exception('Shop does not exist with the given shop name!')


    def shop_manager_permissions_updating(self, token, manager_name_to_update, permission_type, shop_name):
        if self.isToken(token):
            pass

    def shops_roles_info_request(self, shopName, token):
        if self.isToken(token):
            return self._onlineVisitors[token].getRolesInfoReport(shopName)

    def shop_manager_permissions_check(self, manager_name, shop_name, token):
        if self.isToken(token):
            pass

    def is_shop(self, shopName):
        if shopName in self._shops:
            return True
        else:
            raise Exception("Shop does not exist with the given shop name!")

    def payment_execution(self, token): # TODO to specify which params we need
        self._externalServices.execute_payment()

    def shipping_execution(self, token): # TODO to specify which params we need
        self._externalServices.execute_shipment()

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