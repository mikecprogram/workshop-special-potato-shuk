from Dev.DAL.objects.imports import *
from Dev.DAL.objects.DB import *
from Dev.DTO.ShopDTO import ShopDTO
from Dev.DTO.MemberDTO import MemberDTO
from Dev.DTO.CategoryDTO import CategoryDTO
from Dev.DTO.AssignmentDTO import AssignmentDTO
from Dev.DTO.PermissionsDTO import PermissionsDTO
from Dev.DTO.PurchaseHistoryDTO import PurchaseHistoryDTO
from Dev.DTO.StockItemDTO import StockItemDTO
from Dev.DTO.ShoppingCartDTO import ShoppingCartDTO
from Dev.DTO.ShoppingBasketDTO import ShoppingBasketDTO
from Dev.DTO.StockDTO import StockDTO
from DALAssmbler import assembler
import threading
set_sql_debug(True)
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
        return exists(o for o in MemberDAL if MemberDAL.username == name)

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
        return exists(o for o in ShopDAL if ShopDAL.name == name)