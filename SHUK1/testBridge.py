from market import *
from user import *
from membersController import *
class testBridge:
    def __init__(self,market):
        self.market=market
        self.controller=market.getController

m=market()
u=m.enter()
u.getShops()
