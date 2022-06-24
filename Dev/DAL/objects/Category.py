from DB import *
class Category(db.Entity):
    shop = Required("Stock",reverse="categories")
    catagoryName = Required(str)
    catagoryId = Required(int)
    # purchasePolicy = []
    # discountPolicy = []
    stockItems = Set("StockItem")

