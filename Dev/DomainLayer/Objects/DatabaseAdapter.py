from Dev.DAL.Transactions import Transactions
from Dev.DAL.objects.DB import *
from Dev.DTO.ShopDTO import ShopDTO
from Dev.DTO.MemberDTO import MemberDTO
#from Dev.DTO.CategoryDTO import CategoryDTO
from Dev.DTO.AssignmentDTO import AssignmentDTO
from Dev.DTO.PurchaseHistoryDTO import PurchaseHistoryDTO
from Dev.DTO.StockItemDTO import StockItemDTO
from Dev.DTO.ShoppingCartDTO import ShoppingCartDTO
from Dev.DTO.ShoppingBasketDTO import ShoppingBasketDTO
from Dev.DTO.StockDTO import StockDTO
from Dev.DomainLayer.Objects.Permissions import Permissions
from Dev.DomainLayer.Objects.ShoppingCart import ShoppingCart
from Dev.DomainLayer.Objects.Member import Member
from Dev.DomainLayer.Objects.Shop import Shop
from Dev.DomainLayer.Objects.Stock import Stock
from Dev.DomainLayer.Objects.StockItem import StockItem
from Dev.DomainLayer.Objects.Category import Category
from Dev.DomainLayer.Objects.Assignment import Assignment
from Dev.DomainLayer.Objects.ShoppingBasket import ShoppingBasket
from Dev.DomainLayer.Objects.PurchaseHistory import PurchaseHistory
import threading
class DatabaseAdapter:
    def __init__(self):
        self.sequence_number = 1
        self.sequence_number_lock = threading.Lock()
        self.db = Transactions()
        self._membersCache = {}
        self._membersCacheLock = threading.Lock()
        self._shopsCache = {}  # {shopName, shop}
        self._shopsCacheLock = threading.Lock()
        self._stockItemsCache = {}  # {stockitemID, StockItemsDTO}
        self._stockItemsCacheLock = threading.Lock()
        self._ShoppingCartCache = {}  # {memberName, ShoppingCartDTO}
        self._ShoppingCartCacheLock = threading.Lock()
        self._ShoppingBasketCache = {}  # {shopName, ShoppingCartDTO}
        self._ShoppingBasketCacheLock = threading.Lock()

    def add_member(self,username, hashed):
        self.db.add_new_member(username,hashed)

    def add_shop(self,name, founder_name, stock_id, purchase_history_id):
        self.db.add_new_shop(name,founder_name,stock_id,purchase_history_id)

    def get_member(self, name):
        member_DTO = self.db.get_member(name)
        return self.MemberAssmpler(member_DTO,self._increase_sequence_number())

    def _increase_sequence_number(self):
        self.sequence_number_lock.acquire()
        output = self.sequence_number
        self.sequence_number = self.sequence_number+1
        self.sequence_number_lock.release()
        return output

    def is_member(self, name):
        return self.db.is_member(name)

    def get_shop(self, name):
        shop_DTO = self.db.get_shop(name)
        return self.ShopAssmpler(shop_DTO,self._increase_sequence_number())

    def is_shop(self, name):
        return self.is_shop(name)

    def ShopAssmpler(self, shopDTO, seq_num):
        self._shopsCacheLock.acquire()
        if shopDTO.name in self._shopsCache:
            output = self._shopsCache[shopDTO.name]
            if output[1] > 0 and output[1] != seq_num:
                self._shopsCacheLock.release()
                output[0].aqcuire_cache_lock()
                output[0].release__cache_lock()
                return output[0]
            else:
                self._shopsCacheLock.release()
                return output[0]

        output = Shop()
        self._shopsCache[shopDTO.name] = [output, seq_num]
        output.aqcuire_cache_lock()
        self._shopsCacheLock.release()

        output._name = shopDTO.name
        output._stock = self.StockAssmpler(shopDTO.stock, seq_num)
        output._is_open = shopDTO.is_open
        output._founder = self.MemberAssmpler(shopDTO.founder,seq_num)
        output._owners = {key:self.MemberAssmpler(value, seq_num) for key,value in shopDTO.owners.items()}  # {ownerUsername, Member} (ò_ó)!!!!!!!!!!!!!!!!!
        output._managers = {key:self.MemberAssmpler(value, seq_num) for key,value in shopDTO.managers.items()}   # {managerUsername, Member}
        output._purchasePolicies = [] #TODO
        output._discountPolicies = [] #TODO
        output._owners_assignments = {key:[self.AssignmentAssmpler(a) for a in value] for key,value in shopDTO.owners_assignments.items()}
        output._managers_assignments = {key:[self.AssignmentAssmpler(a) for a in value] for key,value in shopDTO.managers_assignments.items()}
        output._purchases_history = self.PurchaseHistoryAssmpler(shopDTO.purchases_history, seq_num)
        #output.notificationPlugin = notificationPlugin #TODO

        self._shopsCacheLock.acquire()
        self._shopsCache[shopDTO.name][1] = -1
        self._shopsCacheLock.release()
        output.release__cache_lock()
        return output

    def MemberAssmpler(self, memberDTO, seq_num):
        self._membersCacheLock.acquire()
        if memberDTO.username in self._membersCache:
            output = self._membersCache[memberDTO.username]
            if output[1] > 0 and output[1] != seq_num:
                self._membersCacheLock.release()
                output[0].aqcuire_cache_lock()
                output[0].release__cache_lock()
                return output[0]
            else:
                self._membersCacheLock.release()
                return output[0]

        output = Member()
        self._membersCache[memberDTO.username] = [output, seq_num]
        output.aqcuire_cache_lock()
        self._membersCacheLock.release()

        output.founded_shops = {key:self.MemberAssmpler(value, seq_num) for key, value in memberDTO.founded_shops.items()}  # {shopName, Shop}
        output.ownedShops = {key:self.MemberAssmpler(value, seq_num) for key, value in memberDTO.ownedShops.items()}  # {shopname, Shop}
        output.managedShops =  {key:self.MemberAssmpler(value, seq_num) for key, value in memberDTO.managedShops.items()}  # load
        output.permissions = {key:Permissions(value) for key, value in memberDTO.managedShops.items()}
        if memberDTO.admin == 0:
            output.admin = None
        else:
            output.admin = memberDTO.admin
        output._username = memberDTO.username
        output._hashed = memberDTO.hashed
        output._savedCart = self.ShoppingCartAssmpler(memberDTO.savedCart,seq_num)
        output._age = memberDTO.age
        output.delayedNoty = memberDTO.delayedNoty

        self._membersCacheLock.acquire()
        self._membersCache[memberDTO.username][1] = -1
        self._membersCacheLock.release()
        output.release__cache_lock()
        return output

    def AssignmentAssmpler(self, assignmentDTO, seq_num):
        output = Assignment(self.MemberAssmpler(assignmentDTO.assigner,seq_num),\
                             self.MemberAssmpler(assignmentDTO.assignee, seq_num))
        output.id = assignmentDTO.id
        return output

    def PurchaseHistoryAssmpler(self, purchaseHistoryDTO, seq_num):
        output =  PurchaseHistory()
        output.purchaseString = purchaseHistoryDTO.purchaseString
        output.id = purchaseHistoryDTO.id
        return output

    def StockItemAssmpler(self, stockItemDTO, seq_num):
        self._stockItemsCacheLock.acquire()
        if stockItemDTO.id in self._stockItemsCache:
            output = self._stockItemsCache[stockItemDTO.id]
            if output[1] > 0 and output[1] != seq_num:
                self._stockItemsCacheLock.release()
                output[0].aqcuire_cache_lock()
                output[0].release__cache_lock()
                return output[0]
            else:
                self._stockItemsCacheLock.release()
                return output[0]

        output = StockItem()
        self._stockItemsCache[stockItemDTO.id] = [output, seq_num]
        output.aqcuire_cache_lock()
        self._stockItemsCacheLock.release()

        output._id = stockItemDTO.id
        output._category = stockItemDTO.category
        output._desc = stockItemDTO.desc
        output._purchasePolicy = []
        output._discountPolicy = []
        output._name = stockItemDTO.name
        output._count = stockItemDTO.count
        output._price = stockItemDTO.price
        output._shopname = stockItemDTO.shopname
        output._id = stockItemDTO.id
        self._stockItemsCacheLock.acquire()
        self._stockItemsCache[stockItemDTO.id][1] = -1
        self._stockItemsCacheLock.release()
        output.release__cache_lock()
        return output

    def ShoppingCartAssmpler(self, shoppingCartDTO, seq_num):
        if shoppingCartDTO is None:
            return None
        self._ShoppingCartCacheLock.acquire()
        if shoppingCartDTO.member.username in self._ShoppingCartCache:
            output = self._ShoppingCartCache[shoppingCartDTO.member.username]
            if output[1] > 0 and output[1] != seq_num:
                self._ShoppingCartCacheLock.release()
                output[0].aqcuire_cache_lock()
                output[0].release__cache_lock()
                return output[0]
            else:
                self._ShoppingCartCacheLock.release()
                return output[0]

        output = ShoppingCart()
        self._ShoppingCartCache[shoppingCartDTO.member.username] = [output, seq_num]
        output.aqcuire_cache_lock()
        self._ShoppingCartCacheLock.release()

        output.member = self.MemberAssmpler(shoppingCartDTO.member, seq_num)
        output.cartPrice = shoppingCartDTO.cartPrice
        output.shoppingBaskets = {key:self.ShoppingBasketAssmpler(value, seq_num) for key, value in shoppingCartDTO.shoppingBaskets.items()}
        output.id = shoppingCartDTO.id

        self._ShoppingCartCacheLock.acquire()
        self._ShoppingCartCache[shoppingCartDTO.member.username][1] = -1
        self._ShoppingCartCacheLock.release()
        output.release__cache_lock()
        return output

    def ShoppingBasketAssmpler(self, shoppingBasketDTO, seq_num):
        self._ShoppingBasketCacheLock.acquire()
        if shoppingBasketDTO.shop.name in self._ShoppingBasketCache:
            output = self._ShoppingBasketCache[shoppingBasketDTO.shop.name]
            if output[1] > 0 and output[1] != seq_num:
                self._ShoppingBasketCacheLock.release()
                output[0].aqcuire_cache_lock()
                output[0].release__cache_lock()
                return output[0]
            else:
                self._ShoppingBasketCacheLock.release()
                return output[0]

        output = ShoppingBasket()
        self._ShoppingBasketCache[shoppingBasketDTO.shop.name] = [output, seq_num]
        output.aqcuire_cache_lock()
        self._ShoppingBasketCacheLock.release()

        output.shoppingCart = self.ShoppingCartAssmpler(shoppingBasketDTO.shoppingCart,seq_num)
        output.shop = self.ShopAssmpler(shoppingBasketDTO.shop,seq_num)
        output.stockItems = shoppingBasketDTO.stockItems
        output.id = shoppingBasketDTO.id
        self._ShoppingBasketCacheLock.acquire()
        self._ShoppingBasketCache[shoppingBasketDTO.shop.name][1] = -1
        self._ShoppingBasketCacheLock.release()
        output.release__cache_lock()
        return output

    def StockAssmpler(self, stockDTO, seq_num):
        output = Stock()
        output._stockItems = {key: self.StockItemAssmpler(value, seq_num) for key, value in stockDTO.stockItems.items()}
        output.id = stockDTO.id
        output.shop_name = stockDTO.id
        return output

class DatabaseAdapterMock:

    def add_member(self,username, hashed):
        pass

    def add_shop(self,name, founder_name, stock_id, purchase_history_id):
        pass

    def get_member(self, name):
        pass

    def is_member(self, name):
        pass

    def get_shop(self, name):
        pass

    def is_shop(self, name):
        pass

database_adapter = DatabaseAdapter()

