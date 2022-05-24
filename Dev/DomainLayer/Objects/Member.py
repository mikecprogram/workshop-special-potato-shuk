#from .Logger import Logger


class Member:

    def __init__(self,username,hashed,market = None):
        self.foundedShops = []#load
        self.ownedShops = []#load
        self.managedShops = []#load
        self.permissions = []#load
        self.assignees = []
        self.admin = market
        self.username=username
        self._hashed = hashed
        
    def get_username(self):
        return self._username

    def set_credintialsHash(self, credintialsHash):
        self._credintialsHash = credintialsHash

    def openShop(self,shop):
        self.foundedShops.append(shop)

    def isHashedCorrect(self,hashed):
        return True if self._hashed == hashed else False
