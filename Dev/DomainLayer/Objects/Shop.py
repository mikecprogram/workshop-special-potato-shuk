from .Logger import Logger
import Stock
import StockItem
import Member
import PurchasePolicy
import DiscountPolicy
import PurchaseHistory
import Assignment

class Shop:

    def ___init___(self,shopName : str,  founder : Member):
        self._name = shopName
        self._stock = Stock()
        self._status = None   # need to confirm if we need shop's status such as closed/open.
        self._founder = founder
        self._owners = None
        self._managers  = None
        self._purchasePolicy = None
        self._discountPolicy = DiscountPolicy()
        self._purchaseHistory = None
        self._assignments = None
        pass # we may need more attributes

    def add_item(self):
        pass

    def remove_item(self):
        pass

    def update_purchase_policy(self):
        pass

    def update_discount_policy(self):
        pass

    def assign_owner(self):
        pass

    def assign_manager(self):
        pass

    def close_shop(self):
        pass





