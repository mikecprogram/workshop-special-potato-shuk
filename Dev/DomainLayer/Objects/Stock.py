#from Dev.DomainLayer.Objects.StockItem import StockItem
from StockItem import StockItem

class Stock:

    def __init__(self):
        self._categories = {}  # {CategoryName, Category}
        self._stockItems = {}  # {stockItemId, stockItem}
        pass
    def getNextId():
        i=1
        while i in self._stockItems.keys():
            i=i+1
        return i
            

    def addCategory(self, category):
        if self._categories.get(category.get_catagoryName()) is None:
            self._categories[category.get_catagoryName()] = category
        else:
            raise Exception('Category is already exist!')

    def addStockItem(self, stockItem: StockItem):
        if self._stockItems.get(stockItem.getID()) is None:
            self._stockItems[stockItem.getID()] = stockItem
        else:
            raise Exception('Stock item is already exist!')

    def removeStockItem(self, stockItemId):
        if self._stockItems.get(stockItemId) is not None:
            self._stockItems.pop(stockItemId)
        else:
            raise Exception('Stock item does not exist!')

    def removeCategory(self, categoryName):
        if self._categories.get(categoryName) is not None:
            self._categories.pop(categoryName)
        else:
            raise Exception('Category does not exist!')

    def get_items_report(self):
        report = 'Items in stock: \n'
        for stockItemId in self._stockItems:
            report += self._stockItems[stockItemId].get_item_report()

        return report
