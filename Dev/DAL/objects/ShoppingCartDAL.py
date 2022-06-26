from  Dev.DAL.objects.DB import *

class ShoppingCartDAL(db.Entity):
    Member = Required("MemberDAL")
    cartPrice = Optional(int)
    shoppingBaskets = Set("ShoppingBasketDAL")
