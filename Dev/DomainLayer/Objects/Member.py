from .Logger import Logger


class Member:

    def __init__(self, user, username, market=None):
        self.user = user
        self.foundedShops = []  # load
        self.ownedShops = {}  # {shopName, shop}
        self.managedShops = {}  # {shopName, shop}
        self.permissions = None  # load
    def __init__(self,username,hashed,market = None):
        self.foundedShops = []#load
        self.ownedShops = []#load
        self.managedShops = []#load
        self.permissions = []#load
        self.assignees = []
        self.admin = market
        self.username = username

    def register(self, marketid, username, password):
        raise Exception("Unfortunately, a member can't perform registering")

        self.username=username
        self._hashed = hashed

    def get_username(self):
        return self._username

    def set_credintialsHash(self, credintialsHash):
        self._credintialsHash = credintialsHash

    def addFoundedShop(self, shop):
        self.foundedShops.append(shop)

    def isHashedCorrect(self,hashed):
        return True if self._hashed == hashed else False

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
