# from .Logger import Logger
import threading
from Dev.DAL.Transactions import t
class PurchaseHistory():

    def __init__(self,save = True ):
        self.id =-1
        if save:
            self.id = t.add_new_purchase_history_rid()
            if self.id == 2:
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.purchaseString = ""
        self._cache_lock = threading.Lock()

    def aqcuire_cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.acquire()

    def release__cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.release()

    def append(self, data):
        raise Exception("DEPRECATED")

    def add(self,userstate,itemname,itemcount,bought_price,atomic = False,atomicId=-1):
        self.purchaseString += "User '%s' bought %d of %s for %f.\n"%(userstate,itemcount,itemname,bought_price)
        if not atomic:
            t.change_purchase_string(self.id, self.purchaseString)
        else:
            t.add_to_atomic(atomicId,lambda:t.change_purchase_string(self.id, self.purchaseString))

    def get_string(self):
        return self.purchaseString
