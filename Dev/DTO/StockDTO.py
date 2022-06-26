# from Dev.DomainLayer.Objects.StockItem import StockItem
from Dev.DomainLayer.Objects.StockItem import *


class StockDTO:

    def __init__(self, stockItems= None):
        self.stockItems = stockItems  # {stockItemName, stockItem}

