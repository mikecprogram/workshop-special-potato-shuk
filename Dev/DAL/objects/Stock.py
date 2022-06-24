from DB import *

class Stock(db.Entity):
    categories = set("Category")
    stockItems = set("StockItem")
