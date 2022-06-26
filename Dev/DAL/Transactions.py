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
    def add_member(self,username, hashed):
        MemberDAL(username=username,hashed=hashed)

    @db_session
    def add_shop(self,name, founder_name, stock_id, purchase_history_id):
        ShopDAL(name = name,stock = StockDAL[stock_id],founder=MemberDAL.get(username=founder_name),\
        purchases_history = PurchaseHistoryDAL[purchase_history_id])

    @db_session
    def add_Stock(self,stock_id):
        StockDAL(id=stock_id)

    @db_session
    def add_purchase_history(self, id):
        PurchaseHistoryDAL(id = id)

    @db_session
    def add_assignment(self, assigner_name,assignee_name):
        PurchaseHistoryDAL(id=id,)

    @db_session
    def add_delayedNoty(self, delayedNoty_id):
        StockDAL(id=stock_id)

    @db_session
    def add_permission(self, id):
        PurchaseHistoryDAL(id=id)

    @db_session
    def add_purchase_history(self, id):
        PurchaseHistoryDAL(id=id)


