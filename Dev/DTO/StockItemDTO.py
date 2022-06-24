from unicodedata import category


##from .Logger import Logger


class StockItemDTO:

    def __init__(self, ID, category: str, name, description, count, purchasepolicy, discountpolicy, price, shopname):
        self.id = ID
        self.category = category
        self.desc = description
        self.purchasePolicy = []
        self.discountPolicy = []
        self.name = name
        self.count = count
        self.price = price
        self.shopname = shopname