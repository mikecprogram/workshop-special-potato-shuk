# from .Logger import Logger


class PurchaseHistory():

    def __init__(self):
        self.purchaseString = ""  # load
        pass

    def append(self, data):
        raise Exception("DEPRECATED")

    def add(self,userstate,itemname,itemcount,bought_price):
        self.purchaseString += "User '%s' bought %d of %s for %f.\n"%(userstate,itemcount,itemname,bought_price)

    def get_string(self):
        return self.purchaseString
