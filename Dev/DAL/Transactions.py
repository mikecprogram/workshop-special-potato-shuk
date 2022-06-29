from Dev.DAL.objects.imports import *
from pony.orm import *
#from Dev.DomainLayer.Objects.Market import Mock
from Dev.DAL.DALAssmbler import assembler
from Dev.Mock_init import Mock
import threading
#set_sql_debug(True)
transaction_lock = threading.Lock()
compositePoliciesClass = [
        "policyNot", "policyAnd", "policyOr", "policyXor", "policyMax", "policyAdd", "policyIf"
    ]
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
    def add_new_member(self,username, hashed,admin):
        if not admin:
            MemberDAL(username=username,hashed=hashed, admin = 0)
        else:
            MemberDAL(username=username, hashed=hashed, admin=1)

    @db_session
    def add_new_shop(self,name, founder_name, stock_id, purchase_history_id):
        ShopDAL(name = name,stock = StockDAL[stock_id],founder=MemberDAL.get(username=founder_name),\
        purchases_history = PurchaseHistoryDAL[purchase_history_id])

    @db_session
    def add_new_Stock_rid(self,shop_name):
        s = StockDAL(shop_name=shop_name)
        s.flush()
        return s.id

    @db_session
    def add_new_purchase_history_rid(self):
        s = PurchaseHistoryDAL(purchaseString='')
        s.flush()
        return s.id

    @db_session
    def add_new_assignment_rid(self, assigner_name,assignee_name):
        s = AssignmentDAL(assigner=MemberDAL.get(username=assigner_name),\
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
    def add_new_shop_basket_rid_if_not_exist(self, shoppingCart_id ,shop_name):
        if not exists(o for o in ShoppingBasketDAL if o.shoppingCart.id == shoppingCart_id and o.shop.name == shop_name):
            print("shop_basket for shopping cart "+str(shoppingCart_id)+"and shop "+shop_name+"didn't exist")
            s = ShoppingBasketDAL(shoppingCart = ShoppingCartDAL[shoppingCart_id],shop = ShopDAL.get(name=shop_name))
            s.flush()
            return s.id
        else:
            print("shop_basket for shopping cart " + str(shoppingCart_id) + "and shop " + shop_name + "exist")
            s = ShoppingBasketDAL.get(shoppingCart=shoppingCart_id, shop=shop_name)
            return s.id

    @db_session
    def get_next_id(self):
        s = AutoIncreamentDal()
        s.flush()
        return s.id

    @db_session
    def add_new_shopping_basket_item_or_change_count(self, ShoppingBasket_id,StockItem_name,count):
        if not exists(o for o in StockItemNameDAL if o.name == StockItem_name):
            s = StockItemNameDAL(name = StockItem_name)
            ShoppingBasketDAL_StockItemDAL(ShoppingBasket = ShoppingBasketDAL[ShoppingBasket_id], StockItemName=s, count=count)
        else:
            s = StockItemNameDAL.get(name = StockItem_name)
            if ShoppingBasketDAL_StockItemDAL.get(ShoppingBasket = ShoppingBasket_id, StockItemName=StockItem_name) is None:
                ShoppingBasketDAL_StockItemDAL(ShoppingBasket = ShoppingBasketDAL[ShoppingBasket_id], StockItemName=s, count=count)
            else:
                s=ShoppingBasketDAL_StockItemDAL.get(ShoppingBasket = ShoppingBasket_id, StockItemName=StockItem_name)
                s.count = count
    @db_session
    def delete_shopping_basket_item_or_change_count(self, ShoppingBasket_id,StockItem_name,removed_count):
        if ShoppingBasketDAL_StockItemDAL.get(ShoppingBasket = ShoppingBasket_id, StockItemName=StockItem_name) is not None:
            s=ShoppingBasketDAL_StockItemDAL.get(ShoppingBasket = ShoppingBasket_id, StockItemName=StockItem_name)
            s.count = s.count - removed_count
            if s.count == 0:
                s.delete()

    @db_session
    def add_new_shopping_cart_rid_if_not_exist(self, member_name):
        if not exists(o for o in ShoppingCartDAL if o.Member.username == member_name):
            print("cart for member "+member_name+"didn't exist")
            s = ShoppingCartDAL(Member = MemberDAL.get(username = member_name))
            s.flush()
            return s.id
        else:
            print("cart for member" + member_name + "exist")
            return ShoppingCartDAL.get(Member=member_name).id


    @db_session
    def add_new_stock_item(self, category, desc , name , count,price,shopname,stock_id):
        s =StockItemDAL(category=category, desc=desc , name=name , count=count,price=price,shopname=shopname,stock=StockDAL[stock_id])
        s.flush()
        return s.id

    @db_session
    def add_shop_manager_assignment(self, shop_name, assignment_id):
        print("add_manager_assignment id: ",assignment_id,"shop_name: ",shop_name)
        ShopDAL.get(name = shop_name).managers_assignments.add(AssignmentDAL[assignment_id])
        print("added_manager_assignment id: ", assignment_id, "shop_name: ", shop_name)

    @db_session
    def add_shop_owner_assignment(self, shop_name, assignment_id):
        print("add_owner_assignment id: ",assignment_id,"shop_name: ",shop_name)
        ShopDAL.get(name=shop_name).owners_assignments.add(AssignmentDAL[assignment_id])
        print("added_owner_assignment id: ",assignment_id,"shop_name: ",shop_name)
    def add_bid(self, bidId,shop_name ,user, itemid, amount, bidPrice):
        BidDAL(id=bidId,shop=shop_name,member=MemberDAL.get(username=user),item=StockItemDAL.get(itemid=itemid),\
        amount=amount,bidPrice=bidPrice)

    def delete_bid(self, bidId):
        BidDAL.get(id=bidId).delete()

    @db_session
    def add_shop_policy(self,policy,shop_name, type1,is_root):
        if PolicyDAL.get(type=type1,isRoot=is_root,ID=policy.ID,shop=shop_name) is None:
            if type(policy).__name__ not in compositePoliciesClass:
                if policy.get_args()[0] is None and policy.get_args()[1] is None:
                    PolicyDAL(type=type1, shop=ShopDAL.get(name=shop_name), ID=policy.ID, name=type(policy).__name__, \
                               percent=policy.percent, \
                              isRoot=is_root)
                    return
                if policy.get_args()[0] is None:
                    PolicyDAL(type=type1, shop=ShopDAL.get(name=shop_name), ID=policy.ID, name=type(policy).__name__, \
                               arg2=policy.get_args()[1],percent=policy.percent, \
                              isRoot=is_root)
                    return
                if policy.get_args()[1] is None:
                    PolicyDAL(type=type1, shop=ShopDAL.get(name=shop_name), ID=policy.ID, name=type(policy).__name__, \
                               arg1=policy.get_args()[0],percent=policy.percent, \
                              isRoot=is_root)
                    return

                PolicyDAL(type=type1,shop=ShopDAL.get(name=shop_name),ID=policy.ID,name=type(policy).__name__,\
                             arg1=policy.get_args()[0],arg2=policy.get_args()[1] , percent= policy.percent,\
                isRoot= is_root)
            else:
                if type(policy).__name__ == "policyNot":
                    arg1=policy.get_args()[0]
                    arg1 = self.add_shop_policy(arg1,shop_name,type1,0)
                    PolicyDAL(type=type1, shop=ShopDAL.get(name=shop_name), ID=policy.ID, name=type(policy).__name__, \
                                     arg1=arg1, percent=policy.percent,\
                                     isRoot = is_root )
                else:
                    arg1 = policy.get_args()[0]
                    self.add_shop_policy(arg1, shop_name, type1, 0)
                    arg2 = policy.get_args()[1]
                    self.add_shop_policy(arg2, shop_name, type1, 0)
                    PolicyDAL(type=type1, shop=ShopDAL.get(name=shop_name), ID=policy.ID, name=type(policy).__name__, \
                                     arg1=str(arg1.ID), arg2=str(arg2.ID), percent=policy.percent, \
                                     isRoot=is_root)
    @db_session
    def delete_shop_policy(self, id, shop_name, type1):
        print(1000,id, shop_name, type1)
        PolicyDAL.get(ID=id, shop=shop_name, type=type1,isRoot = 1).delete()
        print(1000, id, shop_name, type1)
    #--------------------------------------------------------------------

    @db_session
    def delete_member(self, username):
        MemberDAL.get(username=username).delete()

    @db_session
    def delete_shop(self, name):
        ShopDAL.get(name=name).delete()

    @db_session
    def delete_Stock(self,id):
        StockDAL[id].delete()

    @db_session
    def delete_purchase_history(self,id):
        PurchaseHistoryDAL[id].delete()

    @db_session
    def delete_assignment(self, id,name):
        print("\n trying to delete assignment id: ",str(id),name)
        ShopDAL.get(name=name).owners_assignments.remove(AssignmentDAL[id])
        ShopDAL.get(name=name).owners_assignments.remove(AssignmentDAL[id])
        AssignmentDAL[id].delete()
        print("\ndeleted assignment id: ", str(id),name)

    @db_session
    def delete_delayedNoty(self, member_name):
        delete(p for p in DelayedNotyDAL if p.member.username==member_name)

    @db_session
    def delete_permission(self, shop_name, member_name, permission_int):
        PermissionsDAL.get(member = member_name, shop = shop_name,permission = permission_int).delete()


    @db_session
    def delete_shop_basket(self, id):
        ShoppingBasketDAL[id].delete()

    @db_session
    def delete_shopping_basket_item(self, ShoppingBasket_id, StockItem_id):
        ShoppingBasketDAL.get(ShoppingBasket = ShoppingBasket_id,StockItem = StockItem_id).delete()

    @db_session
    def delete_shopping_cart(self, id):
        ShoppingCartDAL[id].delete()

    @db_session
    def delete_stock_item(self, id):
        StockItemDAL[id].delete()

    @db_session
    def change_age(self, member_name,age):
        MemberDAL.get(username = member_name).age = age

    @db_session
    def close_shop(self, shop_name):
        ShopDAL.get(name=shop_name).isOpen = 0

    @db_session
    def reopen_shop(self, shop_name):
        ShopDAL.get(name=shop_name).isOpen = 1

    @db_session
    def addOwnedShop(self, member_name ,shop_name):
        MemberDAL.get(username=member_name).ownedShops.add(ShopDAL.get(name = shop_name))

    @db_session
    def deleteOwnedShop(self, member_name ,shop_name):
        MemberDAL.get(username=member_name).ownedShops.remove(ShopDAL.get(name = shop_name))

    @db_session
    def deleteManagedShop(self, member_name ,shop_name):
        delete(p for p in PermissionsDAL if p.member.username == member_name and p.shop.name == shop_name)

    @db_session
    def item_set_amount(self,item_id, count):
        StockItemDAL[item_id].count = count

    @db_session
    def item_set_name(self, item_id, name):
        StockItemDAL[item_id].name = name

    @db_session
    def item_set_desc(self, item_id, desc):
        StockItemDAL[item_id].desc = desc

    @db_session
    def item_set_price(self, item_id, price):
        StockItemDAL[item_id].price = price

    @db_session
    def item_set_category(self, item_id, category):
        StockItemDAL[item_id].category = category

    @db_session
    def get_all_member_names(self):
        return list(select(m.username for m in MemberDAL))

    @db_session
    def get_all_shop_names(self):
        return list(select(m.name for m in ShopDAL))

    @db_session
    def change_purchase_string(self,id,new_string):
        PurchaseHistoryDAL[id].purchaseString = new_string

class TransactionsMock:
    def add_shop_policy(self, policy, shop_name, type, is_root):
        pass

    def delete_shop_policy(self, id, shop_name, type, is_root=1):
        pass

    def get_member(self, name):
        pass

    def is_member(self, name):
        pass

    def get_shop(self, name):
        pass
    def delete_shopping_basket_item_or_change_count(self, ShoppingBasket_id,StockItem_name,removed_count):
        pass
    def is_shop(self, name):
        pass

    def add_new_member(self, username, hashed, admin):
        pass

    def add_new_shop(self, name, founder_name, stock_id, purchase_history_id):
        pass

    def add_new_Stock_rid(self, shop_name):
        pass

    def add_new_purchase_history_rid(self):
        pass

    def add_new_assignment_rid(self, assigner_name, assignee_name):
        pass

    def add_new_delayedNoty_rid(self, member_name, notification_str):
        pass

    def add_new_permission_rid(self, shop_name, member_name, permission_int):
        pass

    def add_new_shop_basket_rid(self, shoppingCart_id, shop_name):
        pass

    def add_new_shopping_basket_item(self, ShoppingBasket_id, StockItem_name, count):
        pass
    def add_new_shopping_cart_rid(self, member_name):
        pass

    def add_new_stock_item(self, category, desc, name, count, price, shopname, stock_id):
        pass

    def add_shop_manager_assignment(self, shop_name, assignment_id):
        pass

    def add_shop_owner_assignment(self, shop_name, assignment_id):
        pass

    # --------------------------------------------------------------------

    def delete_member(self, username):
        pass

    def delete_shop(self, name):
        pass

    def delete_Stock(self, id):
        pass

    def delete_purchase_history(self, id):
        pass

    def delete_assignment(self, id,name):
        pass

    def delete_delayedNoty(self, member_name):
        pass

    def delete_permission(self, shop_name, member_name, permission_int):
        pass

    def delete_shop_basket(self, id):
        pass

    def delete_shopping_basket_item(self, ShoppingBasket_id, StockItem_id):
        pass

    def delete_shopping_cart(self, id):
        pass

    def delete_stock_item(self, id):
        pass

    def change_age(self, member_name, age):
        pass

    def close_shop(self, shop_name):
        pass

    def reopen_shop(self, shop_name):
        pass

    def addOwnedShop(self, member_name, shop_name):
        pass

    def deleteOwnedShop(self, member_name, shop_name):
        pass

    def deleteManagedShop(self, member_name, shop_name):
        pass

    def item_set_amount(self, item_id, count):
        pass

    def item_set_name(self, item_id, name):
        pass

    def item_set_desc(self, item_id, desc):
        pass

    def item_set_price(self, item_id, price):
        pass

    def item_set_category(self, item_id, category):
        pass

    def get_all_member_names(self):
        pass

    def get_all_shop_names(self):
        pass

    def change_purchase_string(self, id, new_string):
        pass

    def add_new_shop_basket_rid_if_not_exist(self, shoppingCart_id, shop_name):
        pass

    def add_new_shopping_basket_item_or_change_count(self, ShoppingBasket_id, StockItem_name, count):
        pass

    def add_new_shopping_cart_rid_if_not_exist(self, member_name):
        pass


# t = TransactionsMock()
# if not Mock:
if not Mock:
    t = Transactions()
else:
    t = TransactionsMock()