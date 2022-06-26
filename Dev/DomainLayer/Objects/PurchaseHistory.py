# from .Logger import Logger

import threading
class PurchaseHistory():

    def __init__(self):
        self.purchaseString = ""  # load
        self._cache_lock = threading.Lock()

    def aqcuire_cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.acquire()

    def release__cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.release()

    def append(self, data):
        raise Exception("DEPRECATED")

    def add(self,userstate,itemname,itemcount,bought_price):
        self.purchaseString += "User '%s' bought %d of %s for %f.\n"%(userstate,itemcount,itemname,bought_price)

    def get_string(self):
        return self.purchaseString
