from Dev.DAL.objects.imports import *
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
from Dev.DTO.PolicyDTO import PolicyDTO
import threading
compositePoliciesClass = [
        "policyNot", "policyAnd", "policyOr", "policyXor", "policyMax", "policyAdd", "policyIf"
    ]
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
        purchases_history = self.PurchaseHistoryAssmpler(shopDAL.purchases_history)

        output.name = name
        output.stock = stock
        output.is_open = is_open
        output.founder = founder
        output.owners = owners  # {ownerUsername, Member} (ò_ó)!!!!!!!!!!!!!!!!!
        output.managers = managers  # {managerUsername, Member}
        output.purchasePolicies = [self.PolicyAssmpler(sh) for sh in shopDAL.policy if sh.type == "purchase" and sh.isRoot==1]
        output.discountPolicies = [self.PolicyAssmpler(sh) for sh in shopDAL.policy if sh.type == "discount" and sh.isRoot==1]
        output.owners_assignments = owners_assignments_dict
        output.managers_assignments = manager_assignments_dict
        output.purchases_history = purchases_history
        output.bids = {b.id:[b.shop.name,b.member.username,b.item.name,b.amount,b.bidPrice] for b in shopDAL.bids}
        output.bidAccepts = {b.id:set([i.username for i in b.MembersAcceptedBids.members]) for b in shopDAL.bids}
        print("DTOBIds",output.bids)
        print("AccDTOBIds",output.bidAccepts)
        return output

    @db_session
    def MemberAssmpler(self, memberDAL):
        if memberDAL.username in self._membersCache:
            return self._membersCache[memberDAL.username]
        output = MemberDTO(username=memberDAL.username)
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
        output.acceptedBids = {}
        for b in memberDAL.MembersBids:
            if set(select(o.username for o in b.shop.owners)).issubset(set(select(o.username for o in b.MembersAcceptedBids.members))):
                output.acceptedBids[b.id] = [b.shop.name,b.member.username,b.item.name,b.amount,b.bidPrice]
        print("MemberDTOAccBIds", output.acceptedBids)
        return output

    @db_session
    def AssignmentAssmpler(self, assignmentDAL):
        print("AssignmentAssmpler: ",assignmentDAL.assigner.username)
        print("AssignmentAssmpler: ", assignmentDAL.assignee.username)
        print("AssignmentAssmpler: ", str(assignmentDAL.id))
        return AssignmentDTO(self.MemberAssmpler(assignmentDAL.assigner), self.MemberAssmpler(assignmentDAL.assignee),assignmentDAL.id)


    @db_session
    def PurchaseHistoryAssmpler(self, purchaseHistoryDAL):
        return PurchaseHistoryDTO(purchaseHistoryDAL.purchaseString, purchaseHistoryDAL.id)

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
        if shoppingCartDAL is None:
            return None
        if shoppingCartDAL.Member.username in self._ShoppingCartCache:
            return self._ShoppingCartCache[shoppingCartDAL.Member.username]
        output = ShoppingCartDTO()
        self._ShoppingCartCache[shoppingCartDAL.Member.username] = output

        output.member = self.MemberAssmpler(shoppingCartDAL.Member)
        output.cartPrice = shoppingCartDAL.cartPrice
        output.shoppingBaskets ={sb.shop.name:self.ShoppingBasketAssmpler(sb) for sb in shoppingCartDAL.shoppingBaskets}
        output.id = shoppingCartDAL.id
        return output

    @db_session
    def ShoppingBasketAssmpler(self, shoppingBasketDAL):
        if shoppingBasketDAL.id in self._ShoppingBasketCache:
            return self._ShoppingBasketCache[shoppingBasketDAL.id]
        output = ShoppingBasketDTO()
        self._ShoppingBasketCache[shoppingBasketDAL.id] = output
        output.shop = self.ShopAssmpler(shoppingBasketDAL.shop)
        output.stockItems = {sb.StockItemName.name:sb.count for sb in shoppingBasketDAL.ShoppingBasketDAL_StockItemDAL}
        output.shoppingCart = self.ShoppingCartAssmpler(shoppingBasketDAL.shoppingCart)
        output.id = shoppingBasketDAL.id
        return output
    @db_session
    def StockAssmpler(self, stockDAL):
        return StockDTO({si.name:self.StockItemAssmpler(si) for si in stockDAL.stockItems},stockDAL.id,stockDAL.shop_name)



    @db_session
    def PolicyAssmpler(self, policyDAL):
        if policyDAL.name not in compositePoliciesClass:
            return PolicyDTO(policyDAL.percent,policyDAL.shop.name,policyDAL.type,policyDAL.ID,policyDAL.name,\
                            policyDAL.arg1,policyDAL.arg2)
        else:
            if policyDAL.name == "policyNot":
                arg1 = PolicyDAL.get(ID = int(policyDAL.arg1),shop = policyDAL.shop.name,type = policyDAL.type,isRoot = 0)
                arg1 = self.PolicyAssmpler(arg1)
                return PolicyDTO(policyDAL.percent, policyDAL.shop.name, policyDAL.type, policyDAL.ID, policyDAL.name, \
                                 arg1, None)
            else:
                arg1 = PolicyDAL.get(ID=int(policyDAL.arg1), shop=policyDAL.shop.name, type=policyDAL.type,isRoot = 0)
                arg2 = PolicyDAL.get(ID=int(policyDAL.arg2), shop=policyDAL.shop.name, type=policyDAL.type,isRoot = 0)
                arg1 = self.PolicyAssmpler(arg1)
                arg2 = self.PolicyAssmpler(arg2)
                return PolicyDTO(policyDAL.percent, policyDAL.shop.name, policyDAL.type, policyDAL.ID, policyDAL.name, \
                                 arg1, arg2)

    # @db_session
    # def CategoryAssmpler(self, categoryDAL):
    #     return CategoryDTO(self.ShopAssmpler(categoryDAL.shop),categoryDAL.catagoryName,\
    #            categoryDAL.catagoryId,[self.StockItemAssmpler(si) for si in categoryDAL.stockItems])


assembler = DALAssmbler()

