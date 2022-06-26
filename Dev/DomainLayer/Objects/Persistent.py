from abc import abstractmethod


class Persistent():

    def save(self):
        dal = self.toDAL()
        dal.store()

    @abstractmethod
    def fromDAL(self, dal):
        pass

    @abstractmethod
    def toDAL(self):
        pass