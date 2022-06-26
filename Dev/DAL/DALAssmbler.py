from Dev.DAL.objects.imports import *
from Dev.DAL.objects.DB import *
from Dev.DTO.ShopDTO import ShopDTO
from Dev.DTO.MemberDTO import MemberDTO
from Dev.DTO.CategoryDTO import CategoryDTO
from Dev.DTO.AssignmentDTO import AssignmentDTO
from Dev.DTO.PurchaseHistoryDTO import PurchaseHistoryDTO
from Dev.DTO.StockItemDTO import StockItemDTO
from Dev.DTO.ShoppingCartDTO import ShoppingCartDTO
from Dev.DTO.ShoppingBasketDTO import ShoppingBasketDTO
from Dev.DTO.StockDTO import StockDTO
import threading
class DALAssmbler:
    def __init__(self):
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

    @db_session
    def ShopAssmpler(self, shopDAL):
        if shopDAL.name in self._shopsCache:
            return self._shopsCache[shopDAL.name]
        output = ShopDTO()
        self._shopsCache[shopDAL.name] = output
        name = shopDAL.name
        stock = self.StockAssmpler(shopDAL.stock)
        is_open = True
        if shopDAL.isOpen == 0:
            is_open = False
        founder = self.MemberAssmpler(shopDAL.founder)
        owners = {m.username : self.MemberAssmpler(m) for m in shopDAL.owners}
        managers = { p.member.username : self.MemberAssmpler(p.member) for p in shopDAL.permissions}

        owners_assignments = [self.AssignmentAssmpler(oa) for oa in shopDAL.owners_assignments]
        owners_assignments_dict = {oa.assigner.username:[] for oa in owners_assignments}
        for oa in owners_assignments:
            owners_assignments_dict[oa.assigner.username].append(oa)

        manager_assignments = [self.AssignmentAssmpler(ma) for ma in shopDAL.managers_assignments]
        manager_assignments_dict = {ma.assigner.username:[] for ma in manager_assignments}
        for ma in manager_assignments:
            manager_assignments_dict[ma.assigner.username].append(ma)

        purchases_history = shopDAL.purchases_history

        output.name = name
        output.stock = stock
        output.is_open = is_open
        output.founder = founder
        output.owners = owners  # {ownerUsername, Member} (ò_ó)!!!!!!!!!!!!!!!!!
        output.managers = managers  # {managerUsername, Member}
        # self.purchasePolicies = purchasePolicies
        # self.discountPolicies = discountPolicies
        output.owners_assignments = owners_assignments_dict
        output.managers_assignments = manager_assignments_dict
        output.purchases_history = purchases_history
        return output

    @db_session
    def MemberAssmpler(self, memberDAL):
        if memberDAL.username in self._membersCache:
            return self._membersCache[memberDAL.username]
        output = MemberDTO()
        self._membersCache[memberDAL.username] = output
        founded_shops = { fs.name : self.ShopAssmpler(fs)  for fs in memberDAL.foundedShops}
        ownedShops = { os.name : self.ShopAssmpler(os)  for os in memberDAL.ownedShops}
        managedShops  = { p.shop.name : self.ShopAssmpler(p.shop) for p in memberDAL.permissions}  # load
        permissions = { p.shop.name : set() for p in memberDAL.permissions}
        for p in memberDAL.permissions:
            permissions[p.shop.name].add(p.permission)

        admin = memberDAL.admin
        username = memberDAL.username
        hashed = memberDAL.hashed
        savedCart = self.ShoppingCartAssmpler(memberDAL.savedCart)
        age = memberDAL.age
        delayedNoty = [n.notification for n in memberDAL.delayedNotys]

        output.founded_shops = founded_shops
        output.ownedShops = ownedShops
        output.managedShops = managedShops
        output.permissions = permissions
        output.admin = admin
        output.username = username
        output.hashed = hashed
        output.savedCart = savedCart
        output.age = age
        output.delayedNoty = delayedNoty
        return output

    @db_session
    def AssignmentAssmpler(self, assignmentDAL):
        return AssignmentDTO(self.MemberAssmpler(assignmentDAL.assigner), self.MemberAssmpler(assignmentDAL.assignee))


    @db_session
    def PurchaseHistoryAssmpler(self, purchaseHistoryDAL):
        return PurchaseHistoryDTO(purchaseHistoryDAL.purchaseString)

    @db_session
    def StockItemAssmpler(self, stockItemDAL):
        if stockItemDAL.id in self._stockItemsCache:
            return self._stockItemsCache[stockItemDAL.id]
        output = StockItemDTO()
        self._stockItemsCache[stockItemDAL.id] = output

        output.id = stockItemDAL.id
        output.category = stockItemDAL.category
        output.desc = stockItemDAL.desc
        output.name = stockItemDAL.name
        output.count = stockItemDAL.count
        output.price = stockItemDAL.price
        output.shopname = stockItemDAL.shopname

        return output


    @db_session
    def ShoppingCartAssmpler(self, shoppingCartDAL):
        if shoppingCartDAL.Member.username in self._ShoppingCartCache:
            return self._ShoppingCartCache[shoppingCartDAL.Member.username]
        output = ShoppingCartDTO()
        self._ShoppingCartCache[shoppingCartDAL.Member.username] = output

        output.member = self.MemberAssmpler(shoppingCartDAL.Member)
        output.cartPrice = shoppingCartDAL.cartPrice
        output.shoppingBaskets ={sb.shop.name:self.ShoppingBasketAssmpler(sb) for sb in shoppingCartDAL.shoppingBaskets}
        return output

    @db_session
    def ShoppingBasketAssmpler(self, shoppingBasketDAL):
        if shoppingBasketDAL.shop.name in self._ShoppingBasketCache:
            return self._ShoppingBasketCache[shoppingBasketDAL.shop.name]
        output = ShoppingBasketDTO()
        self._ShoppingBasketCache[shoppingBasketDAL.shop.name] = output
        output.shop = self.ShopAssmpler(shoppingBasketDAL.shop)
        output.stockItems = {sb.StockItem.name:sb.count for sb in shoppingBasketDAL.ShoppingBasketDAL_StockItemDAL}
        output.shoppingCart = self.ShoppingCartAssmpler(shoppingBasketDAL.shoppingCart)

    @db_session
    def StockAssmpler(self, stockDAL):
        return StockDTO({si.name:self.StockItemAssmpler(si) for si in stockDAL.stockItems})

    # @db_session
    # def CategoryAssmpler(self, categoryDAL):
    #     return CategoryDTO(self.ShopAssmpler(categoryDAL.shop),categoryDAL.catagoryName,\
    #            categoryDAL.catagoryId,[self.StockItemAssmpler(si) for si in categoryDAL.stockItems])


assembler = DALAssmbler()

