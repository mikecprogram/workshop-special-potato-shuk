from DB import *
class CategoryDAL(db.Entity):
    shop = Required("StockDAL",reverse="categories")
    catagoryName = Required(str)
    catagoryId = Required(int)
    # purchasePolicy = []
    # discountPolicy = []
    stockItems = Set("StockItemDAL")

