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
        self._stocks = []#list of stocks
        self._status = None   # need to confirm if we need shop's status such as closed/open. TODO
        self._founder = founder
        self._owners = []
        self._managers  = []
        self._purchasePolicy = []
        self._discountPolicy = DiscountPolicy()
        self._purchaseHistory = PurchaseHistory()
        self._assignments = {} #hashmap {assigner, [assignees]}

        pass # we may need more attributes

    def add_item(self, item : StockItem):
        self._stock.add(item)

    def remove_item(self, item : StockItem):
                self._stock.remove(item)

    def update_purchase_policy(self):
        pass

    def update_discount_policy(self):
        pass

    def assign_owner(self, assigner, assignee):
        pass

    def assign_manager(self, assigner, assignee):
        pass

    def close_shop(self):
        pass # just change state of shop to closed TODO

    def getTotalDiscount(self, user):
        totaldiscount = 1
        for discount in self._discountPolicy:
            totaldiscount = totaldiscount * discount.getDiscount(user)
        return totaldiscount
    



