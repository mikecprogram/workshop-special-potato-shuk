# from Dev.DomainLayer.Objects.StockItem import StockItem
from Dev.DomainLayer.Objects.StockItem import *


class StockDTO:

    def __init__(self, stockItems= None,id = None,shop_name = None):
        self.id = id
        self.stockItems = stockItems  # {stockItemName, stockItem}
        self.shop_name = shop_name

