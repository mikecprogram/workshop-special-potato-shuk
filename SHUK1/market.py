from membersController import *
from externalSystems import *
from user import *
from shop import shop
from user import user


class market:

    def __init__(self):
        self._id = 1  # need to load from DB
        self._membersController = membersController(self)
        self.activeUsers = []  # used for notifications
        self._shops = []  # load
        self._externalSystems = externalSystems(self)
        self._admins = []  # load

    def getController(self):
        return self._membersController

    def shopByName(self, name):
        for s in self._shops:
            if s.name == name:
                return s
        return None

    def enter(self) -> user:
        u = user(self)
        self.activeUsers.append(u)
        return u

    def exit(self, u):
        self.activeUsers.remove(u)

    def addShop(self, shop):
        # first check no other shop exist in the same name
        for s in self._shops:
            if (s.name == shop.name):
                return False
        self._shops.append(shop)
        return True

    def getShops(self):
        res = []
        for s in self._shops:
            res.append[s.name]
        return res

    def getShopDetails(self, shopname):
        self.shopByName(shopname).details

    def search(self, name, category, keyword, maxPrice, minItemRating, minShopRating):
        r = []
        for s in self._shops:
            r.append(s.search(name, category, keyword, maxPrice, minItemRating, minShopRating))
        return r

    def commitPurchase(self, cart):
        for b in cart:
            s = self.shopByName(b.shop)
            for i in b.stockItems:
                if not s.checkPurchase(i[0], i[1], cart.user):
                    return False
        if not self._externalSystems.checkDelivery(cart.user):
            return False
        price = 0
        for b in cart:
            s = self.shopByName(b.shop)
            for i in b.stockItems:
                price += s.getPrice(i[0], i[1])

        if not self._externalSystems.makePayment(price, cart.user):
            return False
        self._externalSystems.makeDelivery(cart.user)
        return True
