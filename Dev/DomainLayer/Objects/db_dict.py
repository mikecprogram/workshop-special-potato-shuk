from collections.abc import MutableMapping
from DatabaseAdapter import database_adapter
from Market import Mock
class TransformedDictMember(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        if key in self.store:
            return self.store[self._keytransform(key)]
        else:
            if database_adapter.is_member(key):
                return database_adapter.get_member(key)
        raise Exception(str(key)+" is not a member")

    def __setitem__(self, key, value):
        database_adapter.add_member(value._username,value._hashed)

    def __delitem__(self, key):
        del self.store[self._keytransform(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def _keytransform(self, key):
        return key

    def __contains__(self, key):
        try:
            self[key]
        except Exception:
            return False
        else:
            return True


class TransformedDictShop(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        if database_adapter.is_shop(key):
            return database_adapter.get_shop(key)
        raise Exception(str(key) + " is not a Shop name")

    def __setitem__(self, key, value):
        database_adapter.add_shop(value._name,value._founder._username,value._stock.id,value._purchases_history.id)

    def __delitem__(self, key):
        del self.store[self._keytransform(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def _keytransform(self, key):
        return key

    def __contains__(self, key):
        try:
            self[key]
        except Exception:
            return False
        else:
            return True

membersDict = {}
shopsDict = {}
if not Mock:
    membersDict = TransformedDictMember()
    shopsDict =TransformedDictShop()
