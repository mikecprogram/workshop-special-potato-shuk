from  Dev.DAL.objects.DB import *
class StockItemDAL(db.Entity):
    category = Required(str)
    desc = Optional(str)
    # purchasePolicy = []
    # discountPolicy = []
    name = Required(str)
    count = Required(int)
    price = Required(float)
    shopname = Required(str)
    stock = Required("StockDAL")
    bidItem = Set("BidDAL")