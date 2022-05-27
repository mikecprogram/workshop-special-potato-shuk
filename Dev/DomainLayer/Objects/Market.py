from operator import is_
import time
import threading
import sys
sys.path.insert(0, r'C:\Users\USER\Documents\GitHub\workshop-special-potato-shuk\Dev\DomainLayer\Objects')

# from Logger import Logger
from Shop import Shop
from User import User
from ExternalServices import ExternalServices

from Member import Member
from Security import Security


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
        self._externalServices = ExternalServices()

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

    def close_shop(self, token):
        if self.isToken(token):
            pass

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

    def general_items_searching(self, token, category, item_keyword, item_maxPrice):
        if self.isToken(token):
            pass

    def info_about_item_in_shop(self, token, itemid, shop_name):
        if self.isToken(token):
            pass

    def addToCart(self, token, itemid, shop_name, amount):
        if self.isToken(token):
            user = self.getUser(token)
            user.addToCart(itemid,shop_name, amount);
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
            pass

    def get_purchase_history(self, token):
        if self.isToken(token):
            pass
    def getUser(self,token):
        return self._onlineVisitors[token]
    def purchase(self,token):
        if self.isToken(token):
            user = self.getUser(token)
            user.purchase()
            return True
        return False
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
                user = self.getUser(token)
                newShop = Shop(shop_name, user.getMember())
                user.shop_open(newShop)
                return True
            else:
                raise Exception("There is already a shop with given name in the market, try another name please!")

    def adding_item_to_the_shops_stock(self, token, item_name, shop_name, category, item_desc, item_price, amount):
        if self.isToken(token):
            if shop_name in self._shops.keys():
                return self._shops[shop_name].add_item(self._members.get(token), item_name, category, item_desc, item_price, amount)
        return False

    def deleting_item_from_shop_stock(self, token, itemid, shop_name, amount):
        if self.isToken(token):
            pass

    def change_items_details_in_shops_stock(self, token, itemid, shop_name, item_desc, item_price, item_amount):
        if self.isToken(token):
            pass

    def shop_owner_assignment(self, token, shop_name, member_name_to_assignUserName):
        if self.isToken(token):
            if self.is_member(member_name_to_assignUserName):
                self._onlineVisitors[token].assign_owner(shop_name, self._members[member_name_to_assignUserName])

            else:
                raise Exception('member does not exist to be assigned!')
        return True

    def shop_manager_assignment(self, token, shop_name, member_name_to_assignUserName):
        if self.isToken(token):
            if self.is_member(member_name_to_assignUserName):
                self._onlineVisitors[token].assign_manager(shop_name, self._members[member_name_to_assignUserName])

            else:
                raise Exception('member does not exist to be assigned!')
        return True

    def shop_closing(self, token, shop_name):
        if self.isToken(token):
            if self._shops[shop_name] is not None:
                self._shops[shop_name].close_shop()
            else:
                raise Exception('Shop does not exist with the given shop name!')
            # TODO need to add members notification about shop closing event

    def shop_manager_permissions_updating(self, token, manager_name_to_update, permission_type, shop_name):
        if self.isToken(token):
            pass

    def shops_roles_info_request(self, shopName, token):
        if self.isToken(token):
            return self._onlineVisitors[token].getRolesInfoReport(shopName)

    def shop_manager_permissions_check(self, manager_name, shop_name, token):
        if self.isToken(token):
            return [1,3,4]
        else:
            return [1,2,5]

    def is_shop(self, shopName):
        if shopName in self._shops:
            return True
        else:
            raise Exception("Shop does not exist with the given shop name!")

    def payment_execution(self, token): # TODO to specify which params we need
        self._externalServices.execute_payment()

    def shipping_execution(self, token): # TODO to specify which params we need
        self._externalServices.execute_shipment()
