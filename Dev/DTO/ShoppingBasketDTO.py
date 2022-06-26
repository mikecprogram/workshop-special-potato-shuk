# from .Logger import Logger
from Dev.DomainLayer.Objects.Shop import Shop


class ShoppingBasketDTO:

    def __init__(self, shoppingCart= None, shop= None, stockItems= None):
        self.shoppingCart = shoppingCart
        self.shop = shop
        self.stockItems = stockItems

