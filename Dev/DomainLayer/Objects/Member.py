from .Logger import Logger

from User import User


class Member(User):

    def __init__(self, user, username, market=None):
        super().__init__(market)
        self.user = user
        self.foundedShops = []  # load
        self.ownedShops = {}  # {shopName, shop}
        self.managedShops = {}  # {shopName, shop}
        self.permissions = None  # load
        self.assignees = []
        self.admin = market
        self.username = username
        self.load()  # ???

    def register(self, marketid, username, password):
        raise Exception("Unfortunately, a member can't perform registering")

    def get_username(self):
        return self._username

    def set_credintialsHash(self, credintialsHash):
        self._credintialsHash = credintialsHash

    def login(self, username, password):
        raise Exception("Unfortunately, a member can't perform login again")

    def addFoundedShop(self, shop):
        self.foundedShops.append(shop)

    def exit(self):
        super().saveShoppingCart()

    def addOwnedShop(self, shop):
        self.ownedShops[shop.getShopName()] = shop

    def addManagedShop(self, shop):
        self.managedShops[shop.getShopName()] = shop

    def can_assign_manager(self):
        return self.permissions.can_assign_manager()

    def canGetRolesInfoReport(self):
        if self.permissions.canGetRolesInfoReport():
            return True
        else:
            raise Exception("")
