from unicodedata import category


##from .Logger import Logger


class StockItemDTO:

    def __init__(self, ID = None, category= None, name= None, description= None, count= None, price= None, shopname= None):
        self.id = ID
        self.category = category
        self.desc = description
        self.name = name
        self.count = count
        self.price = price
        self.shopname = shopname