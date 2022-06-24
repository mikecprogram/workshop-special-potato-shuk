# from .Logger import Logger
import threading

from Dev.DomainLayer.Objects.ShoppingCart import ShoppingCart
from Dev.DomainLayer.Objects.Permissions import Permissions


class MemberDTO:

    def __init__(self, founded_shops,ownedShops,managedShops,savedCart,age,\
        delayedNoty,permissions,username, hashed, market=None):
        self.founded_shops = founded_shops  # {shopName, Shop}
        self.ownedShops = ownedShops  # {shopname, Shop}
        self.managedShops = managedShops  # load
        self.permissions = permissions  # {shopname, Permissions}
        self.admin = market
        self.username = username
        self.hashed = hashed
        self.savedCart = savedCart
        self.age = age
        self.delayedNoty = delayedNoty
