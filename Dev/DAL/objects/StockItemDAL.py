from DB import *
class StockItemDAL(db.Entity):
    id = PrimaryKey(int)
    category = Required("CategoryDAL")
    desc = Optional(str)
    # purchasePolicy = []
    # discountPolicy = []
    name = Required(str)
    count = Required(int)
    price = Required(int)
    shopname = Required(str)
    shoppingBaskets = Set("ShoppingBasketDAL")
    stock = Required("StockDAL")