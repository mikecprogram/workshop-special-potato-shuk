# from .Logger import Logger
import threading
from Dev.DAL.Transactions import t

class Assignment:

    def __init__(self, assigner_member=None, assignee_member=None):
        self.id = t.add_new_assignment_rid(assigner_member._username,assignee_member._username)
        self.assigner = assigner_member
        self.assignee = assignee_member
        self._cache_lock = threading.Lock()
        self.assignmentType = None

    def aqcuire_cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.acquire()

    def release__cache_lock(self):
        '''DB cache usage please don't use it'''
        self._cache_lock.release()