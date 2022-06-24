# from .Logger import Logger
from Dev.DomainLayer.Objects.Shop import Shop


class ShoppingBasketDTO:

    def __init__(self, shoppingCart, shop, stockItems):
        self.shoppingCart = shoppingCart
        self.shop = shop
        self.stockItems = stockItems

