from DB import *

class Stock(db.Entity):
    categories = Set("Category")
    stockItems = Set("StockItem")
    shop = Optional("Shop")

