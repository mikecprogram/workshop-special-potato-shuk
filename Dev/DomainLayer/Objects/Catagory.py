class Category:

    def ___init___(self,shop, catagoryName, catagoryId):
        self._shop = shop
        self._catagoryName = catagoryName
        self._catagoryId = catagoryId
        self._purchasePolicy = [] 
        self._discountPolicy = [] 
        self._stockItems = []
        pass 

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