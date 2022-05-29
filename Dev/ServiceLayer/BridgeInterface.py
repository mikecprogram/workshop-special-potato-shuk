from Response import Response
from typing import List,Set
from ..DomainLayer.Objects.paymentServiceInterface import paymentServiceInterface
from ..DomainLayer.Objects.shippingServiceInterface import shippingServiceInterface
class BridgeInterface:
    def get_into_the_Trading_system_as_a_guest(self) -> Response[int]:
        pass

    def initialization_of_the_system(self, external_payment_service : paymentServiceInterface, external_supplement_service : shippingServiceInterface,
                                     system_admin_name: str, password: str , MaxTimeOnline : int) -> Response[bool]:
        pass

    def is_active(self,user_id) -> Response[bool]:
        pass

    def is_login(self,user_id) -> Response[bool]:
        pass

    def is_member(self,user_id, name) -> Response[bool]:
        pass

    def shipping_request(self, user_id: int, items : List[str]) -> Response[bool]:
        pass

    #guest and member (exit)
    def Trading_system_quitting(self, user_id: int) -> Response[bool]:
        pass

    def registration_for_the_trading_system(self, user_id: int, name: str, password: str) -> Response[bool]:
        pass

    def login_into_the_trading_system(self, user_id: int, name: str, password: str) -> Response[bool]:
        pass

    def info_about_shop_in_the_market_and_his_items_name(self, user_id, shop_name: str) -> Response[List[str]]: #[shop_desc ,item_name1 , item_name2 ...]
        pass

    def info_about_item_in_shop(self, user_id, item_name, shop_name: str) -> Response[List[str]]: #[]
        pass

    #keyword search from name and description
    def general_items_searching(self, user_id:int,item_name: str =None, category:str =None ,item_keyword: str= None, item_maxPrice: int= None) -> Response[List[List[str]]]: #[[shop_name, item_name1] , [shop_name,item_name2] ...]
        pass

    def shopping_carts_add_item(self, user_id: int, item_name: str, shop_name: str, amount : int) -> Response[bool]:
        pass

    def shopping_carts_check_content(self, user_id: int) -> Response[List[List[str]]]: #List[List[str]]: #[[shop_name, item_name1,item_name2..] , [shop_name, item_name1,item_name2..] ...]
        pass

    def shopping_carts_delete_item(self, user_id: int, item_name: str, shop_name: str, amount :int) -> Response[bool]:
        pass

    #guest and member
    def Shopping_cart_purchase(self, user_id: int) -> Response[bool]:
        pass

    def in_shop_purchases_history_request(self, user_id : int) -> Response[List[str]]:
        pass

    def logout(self, user_id: int) -> Response[bool]:
        pass

    def shop_open(self, user_id: int, shop_name: str) -> Response[bool]:
        pass

    def adding_item_to_the_shops_stock(self, user_id: int, item_name: str, shop_name: str,category:str ,item_desc:str ,item_price : int , amount: int) -> Response[bool]:
        pass

    def deleting_item_from_shop_stock(self, user_id: int, item_name: str, shop_name: str, amount:int) -> Response[bool]:
        pass

    def change_items_details_in_shops_stock(self, user_id: int ,item_name: str, shop_name: str ,item_desc:str = None,item_price : int = None, item_amount: int = None) -> Response[bool]:
        pass

    def shop_owner_assignment(self, user_id:int ,shop_name:str, member_name_to_assign: int, ) -> Response[bool]:
        pass

    def shop_manager_assignment(self, user_id: int, shop_name: str, member_name_to_assign: str) -> Response[bool]:
        pass

    def shop_manager_permissions_add(self, user_id: int, manager_name_to_update: str, permission_type: int, shop_name: str) -> Response[bool]:
        pass

    def shop_manager_permissions_delete(self, user_id: int, manager_name_to_update: str, permission_type: int, shop_name: str)-> Response[bool]:
        pass

    def shop_closing(self, user_id: str, shop_name: str):
        pass

    def shop_manager_permissions_check(self, user_id: int, manager_name: str, shop_name: str) -> Response[Set[int]]:
        pass

    def shops_roles_info_request(self, user_id: str, shop_name: str) -> Response[List[List[str]]]:#[[member_name,"Manager"], [member_name,"Owner"]...]
        pass
