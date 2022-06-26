# from .Logger import Logger
import threading


class Assignment:

    def __init__(self, assigner_member=None, assignee_member=None):
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