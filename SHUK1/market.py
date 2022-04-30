from membersController import *
from externalSystems import *
from user import *
class market:
    
    def __init__(self):
        self._id=1 #need to load from DB
        self._membersController = membersController(self)
        self._activeUsers = []#used for notifications
        self._shops = [] #load
        self._externalSystems = externalSystems(self)
        self._admins = []#load

    def shopByName(self,name):
        for s in self._shops:
            if s.name==shopname:
                return s
        return None
    def enter(self):
        u=user(self)
        self._activeUsers.append(u)
        return u
        
    def exit(self):
        self._activeUsers.remove(u)
        
    def getShops(self):
        res=[]
        for s in self._shops:
            res.append[s.name]
        return res

    def getShopDetails(self,shopname):
        self.shopByName(shopname).details

    def search(self,name,category,keyword,maxPrice,minItemRating,minShopRating):
        r=[]
        for s in self._shops:
            r.append(s.search(name,category,keyword,maxPrice,minItemRating,minShopRating))
        return r


    def commitPurchase(self,cart):
        for b in cart:
            s=shopByName(b.shop)
            for i inb.stockItems:
                if not s.checkPurchase(i[0],i[1],cart.user):
                    return False
        if not self._externalSystems.checkDelivery(cart.user):
            return False
        price=0
        for b in cart:
            s=shopByName(b.shop)
            for i inb.stockItems:
                price+=shop.getPrice(i[0],i[1])
        
        if not self._externalSystems.makePayment(price,cart.user):
            return False
        self._externalSystems.makeDelivery(cart.user)
        return True






        
        
