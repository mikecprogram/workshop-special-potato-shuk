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
    def add_new_shop_basket_rid(self, shoppingCart_id ,shop_name):
        s = ShoppingBasketDAL(shoppingCart = ShoppingCartDAL[shoppingCart_id],shop = ShopDAL.get(name=shop_name))
        s.flush()
        return s.id


    @db_session
    def add_new_shopping_basket_item(self, ShoppingBasket_id,StockItem_name,count):
        if not exists(o for o in StockItemNameDAL if o.name == StockItem_name):
            s =StockItemNameDAL(name = StockItem_name)
            ShoppingBasketDAL_StockItemDAL(ShoppingBasket = ShoppingBasketDAL[ShoppingBasket_id], StockItemName=s, count=count)
        else:
            s = StockItemNameDAL.get(name = StockItem_name)
            ShoppingBasketDAL_StockItemDAL(ShoppingBasket = ShoppingBasketDAL[ShoppingBasket_id], StockItemName=s, count=count)

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

    @db_session
    def add_shop_manager_assignment(self, shop_name, assignment_id):
        ShopDAL.get(name = shop_name).managers_assignments.add(AssignmentDAL[assignment_id])

    @db_session
    def add_shop_owner_assignment(self, shop_name, assignment_id):
        ShopDAL.get(name=shop_name).owners_assignments.add(AssignmentDAL[assignment_id])


    @db_session
    def add_shop_policy(self,policy,shop_name, type,is_root):
        if type(policy).__name__ not in compositePoliciesClass:
             PolicyDAL(type=type,shop=ShopDAL.get(name=shop_name),ID=policy.id,name=policy.name,\
                             arg1=policy.get_args()[0],arg2=policy.get_args()[1] , percent= policy.discount,\
             isRoot= is_root)
        else:
            if type(policy).__name__ == "policyNot":
                arg1=policy.get_args()[0]
                arg1 = self.add_shop_policy(arg1,shop_name,type,0)
                PolicyDAL(type=type, shop=ShopDAL.get(name=shop_name), ID=policy.id, name=policy.name, \
                                 arg1=arg1, arg2=None, percent=policy.discount,\
                                 isRoot = is_root )
            else:
                arg1 = policy.get_args()[0]
                arg1 = self.add_shop_policy(arg1, shop_name, type, 0)
                arg2 = policy.get_args()[1]
                arg2 = self.add_shop_policy(arg2, shop_name, type, 0)
                PolicyDAL(type=type, shop=ShopDAL.get(name=shop_name), ID=policy.id, name=policy.name, \
                                 arg1=arg1, arg2=arg2, percent=policy.discount, \
                                 isRoot=is_root)

    @db_session
    def Delete_shop_policy(self, policy, shop_name, type, is_root):
        pass
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
    def delete_assignment(self, id):
        AssignmentDAL[id].delete()

    @db_session
    def delete_delayedNoty(self, member_name, notification_str):
        list(DelayedNotyDAL.select(lambda p: p.notification==notification_str and p.member==member_name))[0].delete()

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
        delete(p for p in PermissionsDAL if p.member == member_name and p.shop == shop_name)

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
    
    def Delete_shop_policy(self, policy, shop_name, type, is_root):
        pass

    def get_member(self, name):
        pass

    def is_member(self, name):
        pass

    def get_shop(self, name):
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

    def delete_assignment(self, id):
        pass

    def delete_delayedNoty(self, member_name, notification_str):
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
# t = TransactionsMock()
# if not Mock:
if not Mock:
    t = Transactions()
else:
    t = TransactionsMock()