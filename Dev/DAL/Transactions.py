from Dev.DAL.objects.imports import *
from Dev.DAL.objects.DB import *
from Dev.DTO.ShopDTO import ShopDTO
from Dev.DTO.MemberDTO import MemberDTO
from Dev.DTO.CategoryDTO import CategoryDTO
from Dev.DTO.AssignmentDTO import AssignmentDTO
#from Dev.DTO.PermissionsDTO import PermissionsDTO
from Dev.DTO.PurchaseHistoryDTO import PurchaseHistoryDTO
from Dev.DTO.StockItemDTO import StockItemDTO
from Dev.DTO.ShoppingCartDTO import ShoppingCartDTO
from Dev.DTO.ShoppingBasketDTO import ShoppingBasketDTO
from Dev.DTO.StockDTO import StockDTO
from  Dev.DAL.DALAssmbler import assembler
import threading
#set_sql_debug(True)
transaction_lock = threading.Lock()
class Transactions:

    @db_session
    def get_member(self,name):
        if self.is_member(name):
            transaction_lock.acquire()
            output = assembler.MemberAssmpler(MemberDAL.get(username=name))
            transaction_lock.release()
            return output
        else:
            raise Exception("member: "+str(name)+"doesn't exist")
    @db_session
    def is_member(self, name):
        return exists(o for o in MemberDAL if o.username == name)

    @db_session
    def get_shop(self, name):
        if self.is_shop(name):
            transaction_lock.acquire()
            output = assembler.ShopAssmpler(ShopDAL.get(name=name))
            transaction_lock.release()
            return output
        else:
            raise Exception("shop: "+str(name) + " doesn't exist")

    @db_session
    def is_shop(self, name):
        return exists(o for o in ShopDAL if o.name == name)

    @db_session
    def add_new_member(self,username, hashed):
        MemberDAL(username=username,hashed=hashed)

    @db_session
    def add_new_shop(self,name, founder_name, stock_id, purchase_history_id):
        ShopDAL(name = name,stock = StockDAL[stock_id],founder=MemberDAL.get(username=founder_name),\
        purchases_history = PurchaseHistoryDAL[purchase_history_id])

    @db_session
    def add_new_Stock_rid(self,stock_id):
        s = StockDAL()
        s.flush()
        return s.id

    @db_session
    def add_new_purchase_history_rid(self):
        s = PurchaseHistoryDAL(purchaseString="")
        s.flush()
        return s.id

    @db_session
    def add_new_assignment_rid(self, assigner_name,assignee_name):
        s =PurchaseHistoryDAL(assigner=MemberDAL.get(username=assigner_name),\
                           assignee =MemberDAL.get(username=assignee_name) )
        s.flush()
        return s.id

    @db_session
    def add_new_delayedNoty_rid(self, member_name,notification_str):
        s = DelayedNotyDAL(notification=notification_str, member = MemberDAL.get(username=member_name))
        s.flush()
        return s.id

    @db_session
    def add_new_permission_rid(self, shop_name, member_name, permission_int):
        s = PermissionsDAL(member = MemberDAL.get(username=member_name) ,\
                           shop = ShopDAL.get(name=shop_name),permission =permission_int)
        s.flush()
        return s.id

    @db_session
    def add_new_shop_basket_rid(self, shoppingCart_id ,shop_name):
        s = ShoppingBasketDAL(shoppingCart = ShoppingCartDAL[shoppingCart_id],shop = ShopDAL.get(name=shop_name))
        s.flush()
        return s.id

    ShoppingBasket = Required("ShoppingBasketDAL")
    StockItem = Required("StockItemDAL")
    count = Required(int)
    @db_session
    def add_new_shopping_basket_item(self, ShoppingBasket_id,StockItem_id,count):
        ShoppingBasketDAL_StockItemDAL(ShoppingBasket = ShoppingBasket_id, StockItem=StockItem_id, count=count)

    @db_session
    def add_new_shopping_cart_rid(self, member_name):
        s =ShoppingCartDAL(Member = MemberDAL.get(username = member_name))
        s.flush()
        return s.id


    @db_session
    def add_new_stock_item(self, category, desc , name , count,price,shopname,stock_id):
        s =StockItemDAL(category=category, desc=desc , name=name , count=count,price=price,shopname=shopname,stock_id=StockDAL[stock_id])
        s.flush()
        return s.id
