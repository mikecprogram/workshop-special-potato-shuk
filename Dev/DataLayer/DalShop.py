from Dev.DataLayer.DalObject import DalObject


class DalShop(DalObject):

    def __init__(self, shop_name, is_open, founder, policies, items, assignments):
        self.policies = policies
        self.items = items
        self.assignments = assignments
        self._name = shop_name
        self._is_open = is_open
        self._founder = founder

    def store(self):
        pass

    @property
    def is_open(self):
        return self._is_open

    @property
    def name(self):
        return self._name

    @property
    def founder(self):
        return self._founder