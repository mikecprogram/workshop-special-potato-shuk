from DB import *
class Market(db.Entity):
    maxtimeonline = Required(int)
    #self._onlineVisitors = {}  check if need and if yes check
    shops = set("Shop")
    members = set("Member")