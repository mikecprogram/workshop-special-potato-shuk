#from Dev.DomainLayer.Objects.StockItem import StockItem
from Dev.DomainLayer.Objects.StockItem import *

class Stock:

    def __init__(self):
        self._categories = {}  # {CategoryName, Category}
        self._stockItems = {}  # {stockItemId, stockItem}
        pass
    def getNextId(self):
        i=1
        while i in self._stockItems.keys():
            i=i+1
        return i

    def getItemInfo(self,name):
        for k,i in self._stockItems.items():
            if(i.getName()==name):
                return i.toString()
        return None
            

    def addCategory(self, category):
        if self._categories.get(category.get_catagoryName()) is None:
            self._categories[category.get_catagoryName()] = category
        else:
            raise Exception('Category is already exist!')

    def addStockItem(self, stockItem: StockItem):
        if self._stockItems.get(stockItem.getID()) is None:
            self._stockItems[stockItem.getID()] = stockItem
            return True
        else:
            raise Exception('Stock item is already exist!')

    def removeStockItem(self, itemname, amount):
        for n,i in self._stockItems.items():
            if i.getName()==itemname:
                #print(1111)
                if i.getCount()<amount:
                    raise Exception('Not enough items in stock!')
                if i.getCount()==amount:
                    self._stockItems.pop(n)
                self._stockItems[n].remove(amount)
        return True

    def editStockItem(self,itemname, new_name, item_desc, item_price):
        for n, i in self._stockItems.items():
            if i.getName() == itemname:

                if new_name is not None:
                    i.setName(new_name)
                if item_desc is not None:
                    i.setDesc(item_desc)
                if item_price is not None:
                    i.setPrice(item_price)
        return True

    def removeCategory(self, categoryName):
        if self._categories.get(categoryName) is not None:
            self._categories.pop(categoryName)
        else:
            raise Exception('Category does not exist!')

    def get_items_report(self):
        report = []
        for stockItemId in self._stockItems:
            report.append(self._stockItems[stockItemId].getName())

        return report
    
    def search(self, item_name, category, item_keyword, item_maxPrice, name):
        ret=[]
        
        for i,item in self._stockItems.items():
            c=item.getCategory()
            n=item.getName()
            p=item.getPrice()
            d=item.getDesc()
            #print(n,p,item_maxPrice)
            if category is not None and not c==category:
                continue
            if item_name is not None and not n==item_name:
                continue
            if item_maxPrice is not None and p>item_maxPrice:
                continue
            if item_keyword is not None:
                if(item_keyword not in c and item_keyword not in n and item_keyword not in d):
                    continue
            ret.append([name,n])
        #print(ret)
        return ret                


        
