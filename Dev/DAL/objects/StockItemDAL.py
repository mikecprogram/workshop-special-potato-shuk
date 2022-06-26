from DB import *
class StockItemDAL(db.Entity):
    id = PrimaryKey(int)
    category = Required(str)
    desc = Optional(str)
    # purchasePolicy = []
    # discountPolicy = []
    name = Required(str)
    count = Required(int)
    price = Required(int)
    shopname = Required(str)
    ShoppingBasketDAL_StockItemDAL = Set("ShoppingBasketDAL_StockItemDAL")
    stock = Required("StockDAL")