# from Dev.DomainLayer.Objects.StockItem import StockItem
from Dev.DomainLayer.Objects.StockItem import *


class StockDTO:

    def __init__(self, stockItems= None,id = None):
        self.id = id
        self.stockItems = stockItems  # {stockItemName, stockItem}

