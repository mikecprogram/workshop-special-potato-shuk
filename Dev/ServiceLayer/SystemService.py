from BridgeInterface import BridgeInterface
from ..DomainLayer.Controllers.Market import Market as market
from Response import Response
from typing import List,Set
#C:\Users\salih_kadry\Desktop\ServiceLayerV1\workshop-special-potato-shuk\AcceptanceTests
class SystemService(BridgeInterface):
    def __init__(self):
        self.market: market = None

    def get_into_the_Trading_system_as_a_guest(self) -> Response[int]:
        try:
            return Response(self.market.enter())
        except Exception as e:
            return Response(exception=e.__str__())

    def initialization_of_the_system(self, external_payment_service : str, external_supplement_service : str, system_admin_name:str , password :str) -> Response[bool]:
        try:
            self.market: market = market(external_payment_service,external_supplement_service, system_admin_name, password)
            return Response(True)
        except Exception as e:
            return Response(exception=e.__str__())

    def shipping_request(self, user_id: int, items : List[str]) -> Response[bool]:#TODO
        try:
            return Response(self.market.shipping_request(user_id, items))
        except Exception as e:
            return Response(exception=e.__str__())

    def is_active(self, user_id) -> Response[bool]:
        try:
            return Response(self.market.is_active(user_id))
        except Exception as e:
            return Response(exception=e.__str__())

    def is_login(self, user_id) -> Response[bool]:
        try:
            return Response(self.market.is_login(user_id))
        except Exception as e:
            return Response(exception=e.__str__())

    def is_member(self, name) -> Response[bool]:
        try:
            return Response(self.market.is_member(name))
        except Exception as e:
            return Response(exception=e.__str__())

    #guest and member
    def Trading_system_quitting(self, user_id: int) -> Response[bool]:
        try:
           return Response(self.market.exit(user_id))
        except Exception as e:
            return Response(exception=e.__str__())

    def registration_for_the_trading_system(self, user_id: int, name: str, password: str) -> Response[bool]:
        try:
            return Response(self.market.register(user_id, name, password))
        except Exception as e:
            return Response(exception=e.__str__())

    def login_into_the_trading_system(self, user_id: int, name: str, password: str) -> Response[bool]:
        try:
            return Response(self.market.login(user_id, name, password))
        except Exception as e:
            return Response(exception=e.__str__())

    def info_about_shop_in_the_market_and_his_items_name(self, user_id, shop_name: str) -> Response[List[str]]:#[shop description ,item_name1 , item_name2 ...]
        try:
            return Response(self.market.info_about_shop_in_the_market_and_his_items_name(user_id, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def info_about_item_in_shop(self, user_id, item_name, shop_name: str) -> str:
        try:
            return Response(self.market.info_about_item_in_shop(user_id, item_name,shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def general_items_searching(self, user_id:int,item_name: str =None, category:str =None ,item_keyword: str= None, item_maxPrice: int= None)->Response[List[List[str]]]: #[[shop_name, item_name1] , [shop_name,item_name2] ...]
        try:
            return Response(self.market.general_items_searching(user_id,category, item_keyword, item_maxPrice))
        except Exception as e:
            return Response(exception=e.__str__())


    def shopping_carts_add_item(self, user_id: int, item_name: str, shop_name: str, amount:int) -> Response[bool]:
        try:
            return Response(self.market.shopping_carts_add_item(user_id, item_name, shop_name,amount))
        except Exception as e:
            return Response(exception=e.__str__())

    def shopping_carts_check_content(self, user_id: int) -> Response[List[List[str]]]: #List[List[str]]: #[[shop_name, item_name1,item_name2..] , [shop_name, item_name1,item_name2..] ...]
        try:
            return Response(self.market.shopping_carts_check_content(user_id))
        except Exception as e:
            return Response(exception=e.__str__())

    def shopping_carts_delete_item(self, user_id: int, item_name: str, shop_name: str ,amount :int) -> Response[bool]:
        try:
            return Response(self.market.shopping_carts_delete_item( user_id, item_name, shop_name,amount))
        except Exception as e:
            return Response(exception=e.__str__())

    #guest and member
    def Shopping_cart_purchase(self, user_id: int) -> Response[bool]:
        try:
            return Response(self.market.Shopping_cart_purchase(user_id))
        except Exception as e:
            return Response(exception=e.__str__())

    def in_shop_purchases_history_request(self, user_id : int) -> Response[List[str]]:
        try:
            return Response(self.market.get_purchase_history())
        except Exception as e:
            return Response(exception=e.__str__())

    def logout(self, user_id: int) -> Response[bool]:
        try:
            return Response(self.market.logout(user_id))
        except Exception as e:
            return Response(response=e.__str__())

    def shop_open(self, user_id: int, shop_name: str) -> Response[bool]:
        try:
            return Response(self.market.shop_open(user_id, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def adding_item_to_the_shops_stock(self, user_id: int, item_name: str, shop_name: str,category:str ,item_desc:str ,item_price : float , amount: int) -> Response[bool]:
        try:
            return Response(self.market.adding_item_to_the_shops_stock(user_id,item_name,shop_name,category,item_desc,item_price,amount))
        except Exception as e:
            return Response(exception=e.__str__())

    def deleting_item_from_shop_stock(self, user_id: int, item_name: str, shop_name: str, amount:int) -> Response[bool]:
        try:
            return Response(self.market.deleting_item_from_shop_stock(user_id, item_name, shop_name,amount))
        except Exception as e:
            return Response(exception=e.__str__())

    def change_items_details_in_shops_stock(self, user_id: int ,item_name: str, shop_name: str ,item_desc:str = None,item_price : float = None , item_amount: int = None) -> Response[bool]:
        try:
            return Response(self.market.change_items_details_in_shops_stock(user_id, item_name, shop_name, item_desc, item_price, item_amount))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_owner_assignment(self, user_id:int ,shop_name:str, member_name_to_assign: int, ) -> Response[bool]:
        try:
            return Response(self.market.shop_owner_assignment(user_id, shop_name, member_name_to_assign))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_manager_assignment(self, user_id: int, shop_name: str, member_name_to_assign: str) -> Response[bool]:
        try:
            return Response(self.market.shop_manager_assignment(user_id, shop_name,member_name_to_assign))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_manager_permissions_add(self, user_id: int, manager_name_to_update: str, permission_type: int, shop_name: str) -> Response[bool]:
        try:
            return Response(self.market.shop_manager_permissions_updating(user_id, manager_name_to_update ,permission_type, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_manager_permissions_delete(self, user_id: int, manager_name_to_update: str, permission_type: int, shop_name: str) -> Response[bool]:
        try:
            return Response(self.market.shop_manager_permissions_updating(user_id,manager_name_to_update, permission_type, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_closing(self, user_id: str, shop_name: str) -> Response[bool]:
        try:
            return Response(self.market.shop_closing(user_id, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def shop_manager_permissions_check(self, user_id: int, manager_name: str, shop_name: str) -> Response[Set[int]]:
        try:
            return Response(self.market.shop_manager_permissions_check(user_id, manager_name, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

    def shops_roles_info_request(self, user_id: str, shop_name: str) -> Response[List[List[str]]]:#[[member_name,"Manager"], [member_name,"Owner"]...]
        try:
            return Response(self.market.shops_roles_info_request(user_id, shop_name))
        except Exception as e:
            return Response(exception=e.__str__())

