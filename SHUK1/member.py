class member:
    def __init__(self,user,username,market = None):
        self.user = user
        self.ownedShops = []#load
        self.foundedShops = []#load
        self.managedShops = []#load
        self.permissions = []#load
        self.assignees = []
        self.admin = market
        self.username=username

    def logout(self):
        pass

