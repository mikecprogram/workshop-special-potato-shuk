from operator import is_
import time
import threading

from Logger import Logger
from Member import Member
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
maxtimeonline = 1#60 * 10  # 10 minutes
class Market():

    def prid(self,txt):
        if debug:
            print(txt)

    def __init__(self, external_payment_service, external_supplement_service, system_admin_name, password,maxtimeonline = 60*10 ):#10 minutes
        self._maxtimeonline = maxtimeonline
        self._members = {}
        self._onlineVisitors = {}  # hashmap
        self._onlineDate = {}  # hashmap  used only by isToken,enter
        self._nextToken = -1
        self._enterLock = threading.Lock()
        self._shops = {} # {shopName, shop}
        self._security = Security()
        self._externalServices = ExternalServices()

    # returns boolean, returns if current date < 10Minutes+_onlineDate[token]
    # if #t update _onlineDate[token]
    # this will be checked before each user function
    #this function returns whether the token is valid
    def isToken(self, token):
        if(not(token in self._onlineVisitors)):
            self.prid("The token was not found")
            return False
        currentTime = time.time()
        if(currentTime - self._onlineDate[token] < self._maxtimeonline):
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
        del self._onlineVisitors[token]
        del self._onlineDate[token]

    def register(self,token, username, password):
        if self.isToken(token):
            user = self._onlineVisitors[token]
            if user.isMember():
                raise Exception("Logged in member can't register for some reason")
            if not self.is_exist_member(username):
                if is_valid_password(password):
                    hashedPassword =self._security.hash(password)
                    member = Member(username, hashedPassword)
                    self._members[username] = member
                    return True
                else:
                    raise Exception('invalid password!')
            else:
                raise Exception('Username is taken!')
        else:
            return False

    def is_exist_member(self, username):
        return self._members.get(username) is not None

    def open_shop(self, token):
        if self.isToken(token):
            pass

    def close_shop(self, token):
        if self.isToken(token):
            pass

    def is_active(self, user_id):
        return self._onlineVisitors.get(user_id) is not None

    def is_logged_in(self, user_id):
        return self._members.get(user_id) is not None and self._onlineVisitors.get(user_id) is not None

    def shipping_request(self, user_id, items, token):
        if self.isToken(token):
            pass

    def logout(self, token):
        if self.isToken(token):
            user = self._onlineVisitors[token]
            user.logout()


    def login(self,token, username, password):
        if self.isToken(token):
            if not(is_valid_password(password)) :
                raise Exception("Password is not valid")
            if username in self._members:
                member = self._members[username]
                hashed = self._security.hash(password)
                if member.isHashedCorrect(hashed):
                    user = self._onlineVisitors[token]
                    user.login(member)

                    return True
                else:
                    raise Exception("Wrong password")
            else:
                raise Exception("No user such as %s" % username)

    def info_about_shop_in_the_market_and_his_items_name(self, user_id, shop_name, token):
        if self.isToken(token):
            pass

    def general_items_searching(self, user_id, category, item_keyword, item_maxPrice, token):
        if self.isToken(token):
            pass

    def info_about_item_in_shop(self, user_id, item_name, shop_name, token):
        if self.isToken(token):
            pass

    def shopping_carts_add_item(self, user_id, item_name, shop_name, amount, token):
        if self.isToken(token):
            pass

    def shopping_carts_check_content(self, user_id, token):
        if self.isToken(token):
            pass

    def shopping_carts_delete_item(self, user_id, item_name, shop_name, amount, token):
        if self.isToken(token):
            pass

    def Shopping_cart_purchase(self, user_id, token):
        if self.isToken(token):
            pass

    def get_purchase_history(self, token):
        if self.isToken(token):
            pass

    def shop_open(self,token, WTF==>requesterUsername, shop_name, token):
        if self.isToken(token):
            if self.is_member(requesterUsername):
                if not (shop_name in self._shops):
                    newShop = Shop(shop_name, requesterUsername)
                    self._shops[shop_name] = newShop
                    self._members[requesterUsername].addFoundedShop(newShop)

    def adding_item_to_the_shops_stock(self, user_id, item_name, shop_name, category, item_desc, item_price, amount, token):
        if self.isToken(token):
                else:
                    raise Exception("There is already a shop with given name in the market, try another name please!")

    def adding_item_to_the_shops_stock(self, user_id, item_name, shop_name, category, item_desc, item_price, amount,
                                       token):
        if self.can_perform_action(token):
            pass

    def deleting_item_from_shop_stock(self, user_id, item_name, shop_name, amount, token):
        if self.isToken(token):
            pass

    def change_items_details_in_shops_stock(self, user_id, item_name, shop_name, item_desc, item_price, item_amount, token):
        if self.isToken(token):
            pass

    def shop_owner_assignment(self,token, requesterUserName, shop_name, member_name_to_assignUserName):
        if self.isToken(token):
            if self.is_member(member_name_to_assignUserName):
                if shop_name in self._shops:
                    self._shops[shop_name].assign_owner(requesterUserName, self._members[member_name_to_assignUserName])
                else:
                    raise Exception('Shop does not exist with the given shop name!')
            else:
                raise Exception('member does not exist to be assigned!')

    def shop_manager_assignment(self,token, requesterUserName, shop_name, member_name_to_assignUserName):
        if self.isToken(token):
            if self.is_member(member_name_to_assignUserName):
                if self.is_shop(shop_name):
                    self._shops[shop_name].assign_manager(requesterUserName,
                                                          self._members[member_name_to_assignUserName])
                else:
                    raise Exception('Shop does not exist with the given shop name!')
            else:
                raise Exception('member does not exist to be assigned!')

    def shop_closing(self, user_id, shop_name, token):
        if self.isToken(token):
            if self._shops[shop_name] is not None:
                self._shops[shop_name].close_shop()
            else:
                raise Exception('Shop does not exist with the given shop name!')
            # TODO need to add members notification about shop closing event

    def shop_manager_permissions_updating(self, user_id, manager_name_to_update, permission_type, shop_name, token):
        if self.isToken(token):
            pass

    def shops_roles_info_request(self, user_id, shop_name, token):
        if self.isToken(token):
            pass
    def shops_roles_info_request(self, username, shopName, token):
        if self.isToken(token):
            if self.is_member(username):
                if self.is_shop(shopName):
                    return self._shops[shopName].getRolesInfoReport(username)

    def shop_manager_permissions_check(self, user_id, manager_name, shop_name, token):
        if self.isToken(token):
            pass

    def is_shop(self, shopName):
        if shopName in self._shops:
            return True
        else:
            raise Exception("Shop does not exist with the given shop name!")

    def payment_execution(self):
        self._externalServices.execute_payment()

    def shipping_execution(self):
        self._externalServices.execute_shipment()