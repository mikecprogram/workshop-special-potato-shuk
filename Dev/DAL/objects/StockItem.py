from DB import *
class StockItem(db.Entity):
    id = PrimaryKey(int)
    category = Required("Category")
    desc = Optional(str)
    # purchasePolicy = []
    # discountPolicy = []
    name = Required(str)
    count = Required(int)
    price = Required(int)
    shopname = Required(str)
    shoppingBaskets = Set("ShoppingBasket")
    stock = Required("Stock")