

class Category:

    def __init__(self, catagoryName):
        self._catagoryName = catagoryName
        self._purchasePolicy = [] 
        self._discountPolicy = [] 
        self._stockItems = []
        pass 

    def add_stockItem(self, newStockItem): # fix stockItem getters and call them in the appropriate way TODO
        if not any(stockItem.getName() == newStockItem.getName() for stockItem in self._stockItems):
            self._stockItems.append(newStockItem)
        else:
            raise Exception("Stock item already exists!")

    def remove_stockItem(self, removedstockItem):# fix stockItem getters and call them in the appropriate way TODO
        if any(stockItem.getName() == removedstockItem.getName() for stockItem in self._stockItems):
            self._stockItems.remove(removedstockItem)
        else:
            raise Exception("Stock item does not exist!")

    def safe_addstockItem(self, newStockItem):
        if not any(stockItem.getName() == newStockItem.getName() for stockItem in self._stockItems):
            self._stockItems.append(newStockItem)

    def safe_removestockItem(self, removedstockItem):
        if any(stockItem.getName() == removedstockItem.getName() for stockItem in self._stockItems):
            self._stockItems.remove(removedstockItem)

    def add_discountPolicy(self, discountPolicy):
        pass

    def remove_discountPolicy(self, discountPolicy):
        pass
    
    def add_purchasePolicy(self, purchasePolicy):
        pass

    def remove_purchasePolicy(self, purchasePolicy):
        pass

    def removeItem(self,item):
        self._stockItems.remove(item)

    def get_catagoryName(self):
        return self._catagoryName
    
    def getTotalDiscount(self, user):
        totaldiscount = 1
        for discount in self._discountPolicy:
            totaldiscount = totaldiscount * discount.getDiscount(user)
        totaldiscount = totaldiscount * self._shop.getTotalDiscount(user)
        return totaldiscount

    def __str__(self) -> str:
        return self._catagoryName()