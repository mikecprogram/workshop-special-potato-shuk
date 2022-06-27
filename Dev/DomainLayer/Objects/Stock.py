# from Dev.DomainLayer.Objects.StockItem import StockItem
from Dev.DomainLayer.Objects.StockItem import *
import threading
from Dev.DAL.Transactions import t
class Stock:

    def __init__(self,shop_name):
        self.id = t.add_new_Stock_rid(shop_name)
        self.shop_name = shop_name
        self._stockItems = {}  # {stockItemName, stockItem}
        self._cache_lock = threading.Lock()

    def aqcuire_cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.acquire()

    def get_item_id_from_name(self,item_name):#DB use please don't use
        if item_name in self._stockItems:
            return self._stockItems[item_name]._id
        else:
            raise Exception("No such item %s in this shop. please delete delete this item from you're cart before logut" % (item_name))

    def release__cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.release()

    def getNextId(self):
        i = 1
        while i in self._stockItems.keys():
            i = i + 1
        return i

    def purchase(self, itemname: str, amount: int):
        '''Removes amount from count of stockItem'''
        if itemname in list(self._stockItems):
            self._stockItems[itemname].remove(amount)
            return 0;
        raise Exception("No such item %s in this shop." % (itemname))

    def getItemInfo(self, name):  ##WTF why the iteration?!
        if name in self._stockItems.keys():
            item = self._stockItems[name]
            return item.get_item_report_dict()
        raise Exception("No such item %s in this shop." % (name))

    def getItem(self, name):
        if name in self._stockItems.keys():
            item = self._stockItems[name]
            return item
        raise Exception("No such item %s in this shop." % (name))

    def addStockItem(self, stockItem: StockItem):
        if not (stockItem._name in self._stockItems.keys()):
            self._stockItems[stockItem._name] = stockItem
            t.add_new_stock_item(stockItem.getCategory(),stockItem.getDesc(),stockItem.getName()\
                                 ,stockItem.getCount(),stockItem.getPrice(),self.shop_name,self.id)
            return True
        else:
            raise Exception('An item with the same name (%s) already exists in this shop' % stockItem._name)

    def removeStockItem(self, itemname):  # DOES WHAT IT SAYS- DELETES THE ENITRE ITEM FROM STOCK!!!
        itemname = itemname.strip()
        if itemname in self._stockItems.keys():
            t.delete_stock_item(self._stockItems[itemname]._id)
            del self._stockItems[itemname]

        else:
            raise Exception('No such item as %s to delete.' % itemname)

    def editStockItem(self, itemname, new_name, item_desc, category, item_price, amount):
        itemname = itemname.strip()
        if itemname in self._stockItems.keys():
            i = self._stockItems[itemname]
            if amount is not None:
                amount = int(amount)
                if amount < 0:
                    raise Exception("Amount of item can't be negative")
                if amount == 0:
                    self.removeStockItem(itemname)
                    return True
                i.setAmount(amount)
                t.item_set_amount(i._id,amount)
            if new_name is not None:
                new_name = new_name.strip()
                if new_name == "":
                    raise Exception("Name of item can't be null")
                if new_name != itemname:
                    if new_name in self._stockItems.values():
                        raise Exception("Cant change name to already existing item with the same name.")
                    else:
                        self._stockItems[new_name] = self._stockItems.pop(itemname)
                        i.setName(new_name)
                        t.item_set_name(i._id, new_name)
            if item_desc is not None:
                item_desc = item_desc.strip()
                if item_desc == "":
                    raise Exception("Description of item can't be null")
                i.setDesc(item_desc)
                t.item_set_desc(i._id, item_desc)
            if item_price is not None:
                item_price = float(item_price)
                if item_price < 0:
                    raise Exception("Price of item can't be negative")
                i.setPrice(item_price)
                t.item_set_price(i._id, item_price)
            if category is not None:
                category = category.strip()
                if category == "":
                    raise Exception("Category of item can't be null")
                i.setCategory(category)
                t.item_set_category(i._id, category)
            return True
        else:
            raise Exception("No such item such as %s" % itemname)

    def getAmount(self,item_name):
        for item in self._stockItems.values():
            if item.getName() == item_name:
                return item.getCount()
        raise Exception('No such item in stock %s' % item_name)

    def checkAmount(self, item_name, amount):
        for item in self._stockItems.values():
            if item.getName() == item_name:
                if item.getCount() < amount:
                    raise Exception('Not enough items in stock!')
                return True
        raise Exception('No such item in stock %s' % item_name)

    def get_items_report(self):
        return [stockItem.get_item_report_dict() for stockItem in self._stockItems.values()]

    def itemExists(self, itemname):
        return itemname in self._stockItems.keys()

    def isAmount(self, itemname, amount):
        if itemname in self._stockItems.keys():
            if self._stockItems[itemname].getCount() >= amount:
                return True
            else:
                return False
        else:
            raise Exception("Item %s does not exist in stock" % itemname)

    def search(self, query, category, item_minPrice, item_maxPrice):

        ret = []
        category = category.lower()
        for item in self._stockItems.values():
            c = item.getCategory().lower()
            n = item.getName().lower()
            p = item.getPrice()
            d = item.getDesc().lower()
            # print(n,p,item_maxPrice)
            if (query in c or query in n or query in d) or query == "":  # at least one match
                if item_minPrice != 0:
                    if p < item_minPrice:
                        continue
                if item_maxPrice != 0:
                    if p > item_maxPrice:
                        continue
                if category != "":
                    if category != c:
                        print("SKIP CATEGORY")
                        continue
                ret.append(item.get_item_report_dict())
        if len(ret) == 0:
            return None
        print(ret)
        return ret

    def getCategories(self):
        cateories = set()
        for i in self._stockItems.values():
            cateories.add(i.getCategory())
        return cateories