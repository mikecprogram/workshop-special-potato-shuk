class market:
    def __init__(self):
        self.membersController = membersController(self)
        self.activeUsers = []#used for notifications
        self.shops = [] #load
        self.externalSystems = externalSystems(self)
        self.admins = []#load


