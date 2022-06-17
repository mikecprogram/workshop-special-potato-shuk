#from Dev.DomainLayer.Objects.StockItem import StockItem
from Dev.DomainLayer.Objects.StockItem import *

class Stock:

    def __init__(self):
        self._categories = {}  # {CategoryName, Category}
        self._stockItems = {}  # {stockItemName, stockItem}
        pass
    def getNextId(self):
        i=1
        while i in self._stockItems.keys():
            i=i+1
        return i
    def purchase(self,itemname:str,amount:int):
        '''Removes amount from count of stockItem'''
        if itemname in list(self._stockItems):
            self._stockItems[itemname].remove(amount)
            return 0;
        raise Exception("No such item %s in this shop." % (itemname))

    def getItemInfo(self,name):##WTF why the iteration?!
        if name in self._stockItems.keys():
            item = self._stockItems[name]
            return item.get_item_report_dict()
        raise Exception("No such item %s in this shop." % (name))

    def getItem(self, name):
        if name in self._stockItems.keys():
            item = self._stockItems[name]
            return item
        raise Exception("No such item %s in this shop." % (name))
            
    def addItemToCategory(self,categoryName,item):
        if not(item.getCategory() is None):
            item.removeCategory()
        if categoryName in self._categories.keys():
            cat = self._categories[categoryName]
            cat.safe_addstockItem(item)
            item.setCategory(cat)
        else:
            self._categories[categoryName] = Category(categoryName)
            cat = self._categories[categoryName]
            cat.safe_addstockItem(item)
            item.setCategory(cat)
            
    def addCategory(self, category):
        if self._categories.get(category.get_catagoryName()) is None:
            self._categories[category.get_catagoryName()] = category
        else:
            raise Exception('Category is already exist!')

    def addStockItem(self,categoryName, stockItem : StockItem):
        if not(stockItem._name in self._stockItems.keys()):
            self._stockItems[stockItem._name] = stockItem
            self.addItemToCategory(categoryName,stockItem)
            return True
        else:
            raise Exception('An item with the same name (%s) already exists in this shop' % stockItem._name)

    def removeStockItem(self, itemname):#DOES WHAT IT SAYS- DELETES THE ENITRE ITEM FROM STOCK!!!
        itemname = itemname.strip()
        if itemname in self._stockItems.keys():
            self._stockItems[itemname].removeCategory()
            del self._stockItems[itemname]
        else:
            raise Exception('No such item as %s to delete.' % itemname)

    def editStockItem(self,itemname, new_name, item_desc,category, item_price,amount):
        if new_name is None:
            raise Exception("Name of item can't be null")
        if item_desc  is None:
            raise Exception("Description of item can't be null")
        if item_price  is None:
            raise Exception("Price of item can't be negative")
        if amount is None:
            raise Exception("Amount of item can't be negative")
        if category is None:
            raise Exception("Category of item can't be null")
        itemname = itemname.strip()
        new_name = new_name.strip()
        item_desc = item_desc.strip()
        category = category.strip()
        amount = int(amount)
        item_price = float(item_price)
        if itemname in self._stockItems.keys():
            i = self._stockItems[itemname]
            if new_name == "":
                    raise Exception("Name of item can't be null")
            if item_desc == "":
                raise Exception("Description of item can't be null")
            if item_price < 0:
                raise Exception("Price of item can't be negative")
            if amount < 0:
                raise Exception("Amount of item can't be negative")
            if category == "":
                raise Exception("Category of item can't be null")
            i.setName(new_name)
            i.setDesc(item_desc)
            i.setPrice(item_price)
            i.setAmount(amount)
            self.addItemToCategory(category,i)
            return True
        else:
            raise Exception("No such item such as %s" % itemname)

    def checkAmount(self,item_name, amount):
        print(item_name)
        for item in self._stockItems.values():
            print(item.getName())
            if item.getName() == item_name:
                if item.getCount() < amount:
                    raise Exception('Not enough items in stock!')
                return True
        raise Exception('No such items in stock! %s' % item_name)

    def removeCategory(self, categoryName):
        if self._categories.get(categoryName) is not None:
            self._categories.pop(categoryName)
        else:
            raise Exception('Category does not exist!')

    def get_items_report(self):
        return [stockItem.get_item_report_dict() for stockItem in self._stockItems.values()]


    def itemExists(self,itemname):
        return itemname in self._stockItems.keys()
    def isAmount(self, itemname, amount):
        if itemname in self._stockItems.keys():
            if self._stockItems[itemname].getCount() >=amount:
                return True
            else:
                return False
        else:
            raise Exception("Item %s does not exist in stock" % itemname)
    def search(self, query,category,item_minPrice, item_maxPrice):
        
        ret=[]
        
        for item in self._stockItems.values():
            c=item.getCategory().get_catagoryName()
            n=item.getName()
            p=item.getPrice()
            d=item.getDesc()
            #print(n,p,item_maxPrice)
            if query in c or query in n or query in d:#at least one match
                if item_minPrice != 0:
                    if p < item_minPrice:
                        continue
                if item_maxPrice != 0:
                    if p > item_maxPrice:
                        continue
                if category != "":
                    if category != c:
                        continue
                ret.append(item.get_item_report_dict())
        if len(ret) == 0:
            return None
        #print(ret)
        return ret


        
