# from Dev.DomainLayer.Objects.StockItem import StockItem
from Dev.DomainLayer.Objects.StockItem import *


class Stock:

    def __init__(self):
        self._stockItems = {}  # {stockItemName, stockItem}
        pass

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
            return True
        else:
            raise Exception('An item with the same name (%s) already exists in this shop' % stockItem._name)

    def removeStockItem(self, itemname):  # DOES WHAT IT SAYS- DELETES THE ENITRE ITEM FROM STOCK!!!
        itemname = itemname.strip()
        if itemname in self._stockItems.keys():
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
            if item_desc is not None:
                item_desc = item_desc.strip()
                if item_desc == "":
                    raise Exception("Description of item can't be null")
                i.setDesc(item_desc)
            if item_price is not None:
                item_price = float(item_price)
                if item_price < 0:
                    raise Exception("Price of item can't be negative")
                i.setPrice(item_price)
            if category is not None:
                category = category.strip()
                if category == "":
                    raise Exception("Category of item can't be null")
                i.setCategory(category)
            return True
        else:
            raise Exception("No such item such as %s" % itemname)

    def checkAmount(self, item_name, amount):
        for item in self._stockItems.values():
            if item.getName() == item_name:
                if item.getCount() < amount:
                    raise Exception('Not enough items in stock!')
                return True
        raise Exception('No such items in stock! %s' % item_name)

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

        for item in self._stockItems.values():
            c = item.getCategory()
            n = item.getName()
            p = item.getPrice()
            d = item.getDesc()
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
                        continue
                ret.append(item.get_item_report_dict())
        if len(ret) == 0:
            return None
        # print(ret)
        return ret
