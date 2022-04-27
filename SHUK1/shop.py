class shop:
    def __init__(self,market,founder):
        self.market = market
        self.founder = founder
        self.owners = []#load
        self.managers = []#load
        self.purchaseHistory = purchaseHistory(self) #load
        self.discountPolicy = discountPolicy(self)#load
        self.purchasePolicy = purchasePolicy(self)#load
        self.stock = [] #load
