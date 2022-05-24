from operator import is_
import time
import threading

from Logger import Logger
from Member import Member
from Shop import Shop
from User import User


def is_valid_password(password):
    if len(password) >= 8:  # need to add constraints on pass TODO
        return True
    else:
        raise Exception("invalid password")  # may add some hint about a valid password TODO


class Market:
    maxtimeonline = 60 * 10  # 10 minutes

    def __init__(self, external_payment_service, external_supplement_service, system_admin_name, password):
        self._members = {}
        self._onlineVisitors = {}  # hashmap
        self._onlineDate = {}  # hashmap  used only by can_perform_action,enter
        self._nextToken = -1
        self._enterLock = threading.Lock()
        self._shops = {} # {shopName, shop}

    # returns boolean, returns if current date < 10Minutes+_onlineDate[token]
    # if #t update _onlineDate[token]
    # this will be checked before each user function
    def can_perform_action(self, token):
        currentTime = time.time()
        if currentTime - self._onlineDate[token] < maxtimeonline:
            self._onlineDate[token] = currentTime
            return True
        else:
            raise Exception("session time run out")

    # sync me on [enter]
    def enter(self):
        # return token id
        # save token id with a user-guest attached
        self._enterLock.acquire()
        self._nextToken = self._nextToken + 1
        currentToken = self._nextToken
        self._onlineVisitors[self._nextToken] = User(self)
        self._onlineDate[self._nextToken] = time.time()
        self._enterLock.release()
        return currentToken

    def exit(self, token):
        self._onlineDate[token] = 0
        pass

    def register(self, username, password, token):
        if self.can_perform_action(token):
            if not self.is_exist_member(username):
                if is_valid_password(password):
                    hashedPassword = password  # TODO: hash this using external class
                    member = Member(username, hashedPassword)
                    self._members[username] = member
                    return True
                else:
                    raise Exception('invalid password!')
            else:
                raise Exception('Username was taken!')
        else:
            return False

    def is_member(self, username):
        return self._members[username] is not None

    def open_shop(self, token):
        if self.can_perform_action(token):
            pass

    def close_shop(self, token):
        if self.can_perform_action(token):
            pass

    def is_active(self, user_id):
        return self._onlineVisitors.get(user_id) is not None

    def is_login(self, user_id):
        return self._members.get(user_id) is not None and self._onlineVisitors.get(user_id) is not None

    def shipping_request(self, user_id, items, token):
        if self.can_perform_action(token):
            pass

    def login(self, user_id, name, password, token):
        if self.can_perform_action(token):
            pass

    def info_about_shop_in_the_market_and_his_items_name(self, user_id, shop_name, token):
        if self.can_perform_action(token):
            pass

    def general_items_searching(self, user_id, category, item_keyword, item_maxPrice, token):
        if self.can_perform_action(token):
            pass

    def info_about_item_in_shop(self, user_id, item_name, shop_name, token):
        if self.can_perform_action(token):
            pass

    def shopping_carts_add_item(self, user_id, item_name, shop_name, amount, token):
        if self.can_perform_action(token):
            pass

    def shopping_carts_check_content(self, user_id, token):
        if self.can_perform_action(token):
            pass

    def shopping_carts_delete_item(self, user_id, item_name, shop_name, amount, token):
        if self.can_perform_action(token):
            pass

    def Shopping_cart_purchase(self, user_id, token):
        if self.can_perform_action(token):
            pass

    def get_purchase_history(self, token):
        if self.can_perform_action(token):
            pass

    def logout(self, user_id):
        pass

    def shop_open(self, user_id, shop_name, token):
        if self.can_perform_action(token):
            self._shops[shop_name] = Shop(user_id, shop_name)

    def adding_item_to_the_shops_stock(self, user_id, item_name, shop_name, category, item_desc, item_price, amount, token):
        if self.can_perform_action(token):
            pass

    def deleting_item_from_shop_stock(self, user_id, item_name, shop_name, amount, token):
        if self.can_perform_action(token):
            pass

    def change_items_details_in_shops_stock(self, user_id, item_name, shop_name, item_desc, item_price, item_amount, token):
        if self.can_perform_action(token):
            pass

    def shop_owner_assignment(self, requesterId, shop_name, member_name_to_assign, token):
        if self.can_perform_action(token):
            if self.is_member(member_name_to_assign):
                if self._shops[shop_name] is not None:
                    self._shops[shop_name].assign_owner(requesterId, member_name_to_assign)
                else:
                    raise Exception('Shop does not exist with the given shop name!')
            else:
                raise Exception('member does not exist to be assigned!')

    def shop_manager_assignment(self, requesterUserName, shop_name, member_name_to_assignUserName, token):
        if self.can_perform_action(token):
            if self.is_member(member_name_to_assignUserName):
                if self._shops[shop_name] is not None:
                    self._shops[shop_name].assign_manager(requesterUserName, self._members[member_name_to_assignUserName])
                else:
                    raise Exception('Shop does not exist with the given shop name!')
            else:
                raise Exception('member does not exist to be assigned!')

    def shop_closing(self, user_id, shop_name, token):
        if self.can_perform_action(token):
            if self._shops[shop_name] is not None:
                self._shops[shop_name].close_shop()
            else:
                raise Exception('Shop does not exist with the given shop name!')
            #TODO need to add members notification about shop closing event

    def shop_manager_permissions_updating(self, user_id, manager_name_to_update, permission_type, shop_name, token):
        if self.can_perform_action(token):
            pass

    def shops_roles_info_request(self, user_id, shop_name, token):
        if self.can_perform_action(token):
            pass

    def shop_manager_permissions_check(self, user_id, manager_name, shop_name, token):
        if self.can_perform_action(token):
            pass
