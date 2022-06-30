

class MemberDTO:

    def __init__(self, founded_shops= None,ownedShops= None,managedShops= None,savedCart= None,age= None,\
        delayedNoty= None,permissions= None,username= None, hashed= None, market=None):
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
        self.acceptedBids ={}