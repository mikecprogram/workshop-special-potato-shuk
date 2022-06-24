from pony.orm import *
from Assignment import Assignment,db
from Category import Category
from Market import Market
from Member import Member
from Permissions import Permissions
from PurchaseHistory import PurchaseHistory
from Shop import Shop
from ShoppingCart import ShoppingCart
from ShoppingBasket import ShoppingBasket
from Stock import Stock
from StockItem import StockItem

def bind():
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    print(db.generate_mapping(create_tables=True))


if __name__ == "__main__":
    bind()