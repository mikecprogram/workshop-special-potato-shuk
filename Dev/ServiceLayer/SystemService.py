from pickle import NONE
import sys
from Dev.ServiceLayer.BridgeInterface import BridgeInterface
from Dev.ServiceLayer.Response import Response
from typing import List, Set

from Dev.DomainLayer.Objects.shippingServiceInterface import shippingServiceInterface
from Dev.DomainLayer.Objects.paymentServiceInterface import paymentServiceInterface
from Dev.DomainLayer.Objects.Market import Market as market
from Dev.DomainLayer.Objects.PaymentService import PaymentService
from Dev.DomainLayer.Objects.ShippingService import ShippingService


class SystemService(BridgeInterface):
    def __init__(self):
        self.market: market = None

    def get_into_the_Trading_system_as_a_guest(self) -> Response[int]:
        try:
            if self.market is None:
                Response(exception="you have to initialize the system")
            return Response(self.market.enter())
        except Exception as e:
            return Response(exception=e.__str__())

    def initialization_of_the_system(self, external_payment_service: paymentServiceInterface = PaymentService(),
                                     external_supplement_service: shippingServiceInterface = ShippingService(),
                                     system_admin_name: str = "Alex", password: str = "Alex_123456",
                                     MaxTimeOnline: int = 10) -> Response[bool]:
        try:
            if self.market is not None:
                Response(exception="system have been initialized before")
            self.market: market = market(external_payment_service, external_supplement_service, system_admin_name,
                                         password, MaxTimeOnline)
            return Response(True)
        except Exception as e:
            return Response(exception=e.__str__())

    def shipping_request(self, user_id: int, username: str, shopname: str) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.shipping_request(user_id, username,
                                                         shopname))  # get shipping details from user of  <username> and items from and items from the shopping basket
        except Exception as e:
            return Response(exception=e.__str__())

    def get_user_age(self, user_id: int) -> Response[int]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_age(user_id))  # get shipping details from user of  <username> and items from and items from the shopping basket
        except Exception as e:
            return Response(exception=e.__str__())

    def set_user_age(self, user_id: int, age: int) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_age(user_id, age))  # get shipping details from user of  <username> and items from and items from the shopping basket
        except Exception as e:
            return Response(exception=e.__str__())

    def is_active(self, user_id) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.is_active(user_id))
        except Exception as e:
            return Response(exception=e.__str__())

    def is_login(self, user_id) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.is_logged_in(user_id))
        except Exception as e:
            return Response(exception=e.__str__())

    def is_member(self, name) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.is_member(name))
        except Exception as e:
            return Response(exception=e.__str__())

    def get_owned_shops(self, user_id, username) -> Response[List[str]]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_owned_shops(user_id, username))
        except Exception as e:
            return Response(exception=e.__str__())

    def get_founded_shops(self, user_id, username) -> Response[List[str]]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_founded_shops(user_id, username))
        except Exception as e:
            return Response(exception=e.__str__())

    def get_managed_shops(self, user_id, username) -> Response[List[str]]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_founded_shops(user_id, username))
        except Exception as e:
            return Response(exception=e.__str__())

    # guest and member
    def Trading_system_quitting(self, token) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            self.market.exit(token)

        except Exception as e:
            return Response(exception=e.__str__())

    def registration_for_the_trading_system(self, user_id: int, name: str, password: str) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.register(user_id, name, password))
        except Exception as e:
            return Response(exception=e.__str__())

    def login_into_the_trading_system(self, user_id: int, name: str, password: str) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.login(user_id, name, password))
        except Exception as e:
            return Response(exception=e.__str__())

    def info_about_shop_in_the_market_and_his_items_name(self, user_id, shop_name: str) -> Response[
        List[str]]:  # [shop description ,item_name1 , item_name2 ...]
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.info_about_shop_in_the_market_and_his_items_name(user_id, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def info_about_item_in_shop(self, user_id, item_name, shop_name: str) -> Response:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.info_about_item_in_shop(user_id, item_name, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def general_items_searching(self, user_id: int, item_name: str = None, category: str = None,
                                item_keyword: str = None, item_maxPrice: int = None) -> Response[
        List[List[str]]]:  # [[shop_name, item_name1] , [shop_name,item_name2] ...]
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(
                self.market.general_items_searching(user_id, item_name, category, item_keyword, item_maxPrice))
        except Exception as e:
            return Response(exception=e.__str__())

    def shopping_carts_add_item(self, user_id: int, item_name: str, shop_name: str, amount: int) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.shopping_carts_add_item(user_id, item_name, shop_name, amount))
        except Exception as e:
            return Response(exception=e.__str__())

    def shopping_carts_check_content(self, user_id: int) -> Response[List[List[
        str]]]:  # List[List[str]]: #[[shop_name, item_name1,item_name2..] , [shop_name, item_name1,item_name2..] ...]
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.getCartContents(user_id))
        except Exception as e:
            return Response(exception=e.__str__())

    def shopping_carts_delete_item(self, user_id: int, item_name: str, shop_name: str, amount: int) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.removeFromCart(user_id, item_name, shop_name, amount))
        except Exception as e:
            return Response(exception=e.__str__())

    # guest and member
    def Shopping_cart_purchase(self, user_id: int) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.Shopping_cart_purchase(user_id))
        except Exception as e:
            return Response(exception=e.__str__())

    def get_cart_price(self, token) -> Response[int]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_cart_price(token))
        except Exception as e:
            return Response(exception=e.__str__())

    def add_policy(self, token, percent, name, arg1=None, arg2=None) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.add_policy(token, percent, name, arg1, arg2))
        except Exception as e:
            return Response(exception=e.__str__())

    def add_purchase_policy_to_shop(self, token, shopname, policyID) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.add_purchase_policy_to_shop(token, shopname, policyID))
        except Exception as e:
            return Response(exception=e.__str__())

    def compose_policy(self, token, name, policy1, policy2=None) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.compose_policy(token, name, policy1, policy2))
        except Exception as e:
            return Response(exception=e.__str__())

    def add_discount_policy_to_shop(self, token, shopname, policyID) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.add_discount_policy_to_shop(token, shopname, policyID))
        except Exception as e:
            return Response(exception=e.__str__())

    def delete_policy(self, token, shopname, policyID)-> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.remove_policy_from_shop(token, shopname, policyID))
        except Exception as e:
            return Response(exception=e.__str__())

    def get_my_policies(self, token) -> Response[List[List[object]]]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_my_policies(token))
        except Exception as e:
            return Response(exception=e.__str__())

    def get_shop_policies(self, token, shopname) -> Response[List[List[object]]]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_shop_policies(token, shopname))
        except Exception as e:
            return Response(exception=e.__str__())


    def in_shop_purchases_history_request(self, token, shopname) -> Response[List[str]]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_inshop_purchases_history(token, shopname))
        except Exception as e:
            return Response(exception=e.__str__())

    def logout(self, user_id: int) -> Response[str]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.logout(user_id))
        except Exception as e:
            return Response(response=e.__str__())

    def shop_open(self, user_id: int, shop_name: str) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.shop_open(user_id, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def adding_item_to_the_shops_stock(self, user_id: int, item_name: str, shop_name: str, category: str,
                                       item_desc: str, item_price: float, amount: int) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(
                self.market.adding_item_to_the_shops_stock(user_id, item_name, shop_name, category, item_desc,
                                                           item_price, amount))
        except Exception as e:
            return Response(exception=e.__str__())

    def validate_purchase_policy(self, user_id: int) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.validate_purchase_policy(user_id))  # market return true if all items in basket fit policy and false if not
        except Exception as e:
            return Response(exception=e.__str__())

    def get_discount(self, user_id: int, shopname: str) -> Response[
        float]:  # market return float of final discount for all items in the shopping *basket* all calcs in domain
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_discount(user_id, shopname))
        except Exception as e:
            return Response(exception=e.__str__())

    def deleting_item_from_shop_stock(self, user_id: int, item_name: str, shop_name: str, amount: int) -> Response[
        bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.deleting_item_from_shop_stock(user_id, item_name, shop_name, amount))
        except Exception as e:
            return Response(exception=e.__str__())

    def change_items_details_in_shops_stock(self, user_id: int, item_name: str, shop_name: str, new_name=None,
                                            item_desc: str = None,
                                            item_price: float = None) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(
                self.market.change_items_details_in_shops_stock(user_id, item_name, shop_name, new_name, item_desc,
                                                                item_price))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_owner_assignment(self, user_id: int, shop_name: str, member_name_to_assign: int, ) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.shop_owner_assignment(user_id, shop_name, member_name_to_assign))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_manager_assignment(self, user_id: int, shop_name: str, member_name_to_assign: str) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.shop_manager_assignment(user_id, shop_name, member_name_to_assign))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_manager_permissions_add(self, user_id: int, manager_name_to_update: str, permission_type: int,
                                     shop_name: str) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(
                self.market.shop_manager_permissions_updating(user_id, manager_name_to_update, permission_type,
                                                              shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_manager_permissions_delete(self, user_id: int, manager_name_to_update: str, permission_type: int,
                                        shop_name: str) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(
                self.market.shop_manager_permissions_updating(user_id, manager_name_to_update, permission_type,
                                                              shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_closing(self, user_id: int, shop_name: str) -> Response[bool]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.shop_closing(user_id, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_manager_permissions_check(self, user_id: int, manager_name: str, shop_name: str) -> Response[List[str]]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.shop_manager_permissions_check(user_id, manager_name, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def shops_roles_info_request(self, username: int, shop_name: str, token) -> Response[
        List[List[str]]]:  # [[member_name,"Manager"], [member_name,"Owner"]...]
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.shops_roles_info_request(username, shop_name, token))

        except Exception as e:
            return Response(exception=e.__str__())

    def get_all_members_name(self, user_id: int) -> Response[List[List[str]]]:#[[online_member_name1,online_member_name2..][offline_member_name1,online_member_name2..]]
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_all_members_name(user_id))

        except Exception as e:
            return Response(exception=e.__str__())

    def get_member_info(self, user_id: int, member_name: str) -> Response[str]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.get_member_info(user_id ,member_name))

        except Exception as e:
            return Response(exception=e.__str__())

    def delete_shop_owner(self, user_id: int, shop_name: str, owner_name: str) -> Response[None]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.delete_shop_owner(user_id, shop_name, owner_name))

        except Exception as e:
            return Response(exception=e.__str__())

    def delete_member(self, user_id: int, member_name: str) -> Response[None]:
        try:
            if self.market is None:
                return Response(exception="you have to initialize the system")
            return Response(self.market.delete_member(user_id, member_name))

        except Exception as e:
            return Response(exception=e.__str__())