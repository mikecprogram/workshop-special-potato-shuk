import threading
class Category:

    def __init__(self,shop=None, catagoryName=None, catagoryId=None):
        self._shop = shop
        self._catagoryName = catagoryName
        self._catagoryId = catagoryId
        self._purchasePolicy = [] 
        self._discountPolicy = [] 
        self._stockItems = []
        self._cache_lock = threading.Lock()

    def aqcuire_cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.acquire()

    def release__cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.release()

    def add_stockItem(self, newStockItem): # fix stockItem getters and call them in the appropriate way TODO
        if not any(stockItem.get_itemId() == newStockItem.get_itemId for stockItem in self._stockItems):
            self._stockItems.append(newStockItem)
        else:
            raise Exception("Stock item already exists!")


    def remove_stockItem(self, removedstockItem):# fix stockItem getters and call them in the appropriate way TODO
        if any(stockItem.get_itemId() == removedstockItem.get_itemId for stockItem in self._stockItems):
            self._stockItems.remove(removedstockItem)
        else:
            raise Exception("Stock item does not exist!")

    
    def add_discountPolicy(self, discountPolicy):
        pass

    def remove_discountPolicy(self, discountPolicy):
        pass
    
    def add_purchasePolicy(self, purchasePolicy):
        pass

    def remove_purchasePolicy(self, purchasePolicy):
        pass


    def get_catagoryId(self):
        return self._catagoryId

    def get_catagoryName(self):
        return self._catagoryName
    
    def getTotalDiscount(self, user):
        totaldiscount = 1
        for discount in self._discountPolicy:
            totaldiscount = totaldiscount * discount.getDiscount(user)
        totaldiscount = totaldiscount * self._shop.getTotalDiscount(user)
        return totaldiscount