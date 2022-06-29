from Dev.DAL.objects.DB import *

class BidDAL(db.Entity):
    id = PrimaryKey(int)
    shop = Required("ShopDAL")
    member = Required("MemberDAL")
    item = Required("StockItemDAL")
    amount = Required(int)
    bidPrice = Required(float)

