##from .Logger import Logger
from hashlib import sha1
from tkinter import E
from Dev.DomainLayer.Objects.ShoppingBasket import ShoppingBasket
from Dev.DomainLayer.Objects.Shop import Shop


class ShoppingCartDTO:

    def __init__(self, user, cartPrice, shoppingBaskets):
        self.user = user
        self.cartPrice = cartPrice
        self.shoppingBaskets = shoppingBaskets
