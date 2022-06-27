from collections.abc import MutableMapping
from DatabaseAdapter import database_adapter
from Market import Mock,Shop,Member
import threading
class ReadWriteLock:
    """ A lock object that allows many simultaneous "read locks", but
    only one "write lock." """

    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    def acquire_read(self):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        self._read_ready.acquire(  )
        try:
            self._readers += 1
        finally:
            self._read_ready.release(  )

    def release_read(self):
        """ Release a read lock. """
        self._read_ready.acquire(  )
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll(  )
        finally:
            self._read_ready.release(  )

    def acquire_write(self):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """
        self._read_ready.acquire(  )
        while self._readers > 0:
            self._read_ready.wait(  )

    def release_write(self):
        """ Release a write lock. """
        self._read_ready.release()


class TransformedDictMember(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.rw = ReadWriteLock()
        self.store = {n: (lambda:database_adapter.get_member(n)) for n in database_adapter.get_all_member_names()}
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        self.rw.acquire_read()
        if key in self.store:
            output = self.store[key]()
            self.rw.release_read()
            return output
        self.rw.release_read()
        raise Exception(str(key)+" is not a member")

    def __setitem__(self, key, value):
        self.rw.acquire_write()
        database_adapter.add_member(value._username,value._hashed)
        self.store[key] = lambda: database_adapter.get_member(key)
        self.rw.release_write()

    def __delitem__(self, key):
        self.rw.acquire_write()
        del self.store[self._keytransform(key)]
        database_adapter.db.delete_member(self._keytransform(key))
        self.rw.release_write()


    def __iter__(self):
        self.rw.acquire_read()
        output = iter(self.store)
        self.rw.release_read()
        return output

    def __len__(self):
        self.rw.acquire_read()
        output = len(self.store)
        self.rw.release_read()
        return output

    def _keytransform(self, key):
        return key
    def keys(self):
        self.rw.acquire_read()
        output = self.store.keys()
        self.rw.release_read()
        return output

    def __contains__(self, key):
        self.rw.acquire_read()
        output = key in self.store
        self.rw.release_read()
        return output

    def values(self):
        self.rw.acquire_read()
        output = [i() for i in self.store.values()]
        self.rw.release_read()
        return output

    def items(self):
        self.rw.acquire_read()
        output= [(key,value(),) for key,value in self.store.items()]
        self.rw.release_read()
        return output
class TransformedDictShop(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.rw = ReadWriteLock()
        self.store = {n:lambda:database_adapter.get_shop(n) for n in database_adapter.get_all_shop_names()}
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        self.rw.acquire_read()
        if key in self.store:
            output = self.store[key]()
            self.rw.release_read()
            return output
        self.rw.release_read()
        raise Exception(str(key) + " is not a Shop name")

    def __setitem__(self, key, value):
        self.rw.acquire_write()
        database_adapter.add_shop(value._name,value._founder._username,value._stock.id,value._purchases_history.id)
        self.store[key] = lambda: database_adapter.get_shop(key)
        self.rw.release_write()

    def __delitem__(self, key):
        self.rw.acquire_write()
        del self.store[self._keytransform(key)]
        database_adapter.db.delete_shop(self._keytransform(key))
        self.rw.release_write()

    def __iter__(self):
        self.rw.acquire_read()
        output = iter(self.store)
        self.rw.release_read()
        return output

    def __len__(self):
        self.rw.acquire_read()
        output = len(self.store)
        self.rw.release_read()
        return output

    def _keytransform(self, key):
        return key

    def keys(self):
        self.rw.acquire_read()
        output = self.store.keys()
        self.rw.release_read()
        return output

    def __contains__(self, key):
        self.rw.acquire_read()
        output = key in self.store
        self.rw.release_read()
        return output

    def values(self):
        self.rw.acquire_read()
        output = [i() for i in self.store.values()]
        self.rw.release_read()
        return output

    def items(self):
        self.rw.acquire_read()
        output = [(key, value(),) for key, value in self.store.items()]
        self.rw.release_read()
        return output

membersDict = {}
shopsDict = {}
if not Mock:
    membersDict = TransformedDictMember()
    shopsDict =TransformedDictShop()

