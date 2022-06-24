from Dev.DAL.objects.imports import *
from Dev.DAL.objects.DB import *
import threading
class transaction:
    def __init__(self):
        self._membersCache = {}
        self._membersCacheLock = threading.Lock()
        self._shopsCache = {}  # {shopName, shop}
        self._shopsCacheLock = threading.Lock()
    @db_session
    def get_member(self,member_name):
        self._membersCacheLock.acquire()
        if member_name in self._membersCache:
            output = self._membersCache[member_name]
            self._membersCacheLock.release()
            return output
        m = MemberDAL.get(username = member_name)



