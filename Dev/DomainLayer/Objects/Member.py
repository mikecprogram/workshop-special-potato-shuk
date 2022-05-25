from .Logger import Logger

from User import User


class Member(User):

    def __init__(self, user, username, market=None):
        super().__init__(market)
        self.user = user
        self.foundedShops = []  # load
        self.ownedShops = []  # load
        self.managedShops = []  # load
        self.permissions = []  # load
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

    def exit(self, token):
        super().saveShoppingCart()
