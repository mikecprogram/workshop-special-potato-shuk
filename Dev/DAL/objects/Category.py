from DB import *
class Category(db.Entity):
    shop = Required("Shop")
    catagoryName = Required(str)
    catagoryId = Required(int)
    purchasePolicy = []
    discountPolicy = []
    stockItems = set("StockItem")

