##from .Logger import Logger
from hashlib import sha1
from tkinter import E
from Dev.DomainLayer.Objects.ShoppingBasket import ShoppingBasket
from Dev.DAL.Transactions import t
import threading
class ShoppingCart:

    def __init__(self, user=None):
        self.id = -1
        self._user = user
        self._cartPrice = None
        self.shoppingBaskets = {}  # {shopName, ShoppingBasket}
        self._cache_lock = threading.Lock()

    def aqcuire_cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.acquire()

    def release__cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.release()

    def getBasketByShop(self, shop):
        if type(shop) is str:
            if shop not in self.shoppingBaskets.keys():
                return None
            return self.shoppingBaskets[shop]
        else:
            if shop.getShopName() not in self.shoppingBaskets.keys():
                return None
            return self.shoppingBaskets[shop.getShopName()]

    def addItem(self, shop, item_name, amount,user):
        s = self.getBasketByShop(shop)
        if s is None:
            s = ShoppingBasket(self, shop)
            self.shoppingBaskets[shop.getShopName()] = s
        s.addItem(item_name, amount)
        if user.isMember():
            self.store()

    def removeItem(self, shopName, item_name, amount,user):
        b = self.getBasketByShop(shopName)
        if b is None:
            raise Exception("Cant remove item from a shop you dont have cart from (%s)" % shopName)
        if b.removeItem(item_name, amount):
            if b.is_empty():
                del self.shoppingBaskets[shopName]
        if user.isMember():
            t.delete_shopping_basket_item_or_change_count(b.id,item_name,amount)
            if b.is_empty():
                t.delete_shop_basket(b.id)
        return True


    def validate_purchase(self):
        for name, basket in self.shoppingBaskets.items():
            if not basket.validate_purchase(self._user):
                return False
        return True

    def calculate_price(self):
        sum = 0
        for name, basket in self.shoppingBaskets.items():
            sum += basket.calculate_price(self._user)
        return sum

    def checkBaskets(self):
        ans = {}
        for name in self.shoppingBaskets:
            b = self.shoppingBaskets[name]
            ans[b.shop.getShopName()] = b.checkBasket()
        return ans

    def checkBasket(self, shopname):
        if shopname in self.shoppingBaskets:
            return self.shoppingBaskets[shopname].checkBasket()

    def getRawPrice(self, shopname):
        if shopname in self.shoppingBaskets:
            return self.shoppingBaskets[shopname].raw_price()

    def clear(self):
        self._user = None
        self._cartPrice = None
        for shop in self.shoppingBaskets:
            self.shoppingBaskets[shop].clear()

    def store(self):
        try:
            self.id = t.add_new_shopping_cart_rid_if_not_exist(self._user.getMember().get_username())
            for shopname,sb in self.shoppingBaskets.items():
                sb.id = t.add_new_shop_basket_rid_if_not_exist(self.id,shopname)
                stock_items = sb.get_stockItems()
                for name,count in stock_items.items():
                    t.add_new_shopping_basket_item_or_change_count(sb.id,name,count)
        except Exception as e:
            print(e.__str__())
            raise e


    def setUser(self, user):
        self._user = user

    def purchase(self):
        try:
            for name in self.shoppingBaskets:
                b = self.shoppingBaskets[name]
                b.purchase(self._user)
            return True
        except Exception as e:
            raise e

    def archive_shopping_baskets(self, token):
        for basket in self.shoppingBaskets.values():
            basket.archive(token)

    def calculate_item_price(self, shop, itemname):
        b = self.getBasketByShop(shop)
        if b is None:
            return shop.calculate_price_for_general_item(self._user, itemname)
        else:
            return b.calculate_item_price(self._user,itemname)
