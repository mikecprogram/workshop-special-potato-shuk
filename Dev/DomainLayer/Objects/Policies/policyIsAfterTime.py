from Dev.DataLayer.DalPolicy import DalPolicy
from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable
import datetime


class policyIsAfterTime(Composable):

    def __init__(self, shopname, ID, percent, hour, minute):
        self.shopname = shopname
        self.ID = ID
        self.percent = float(percent)
        self.hour = int(hour)
        self.minute = int(minute)

    def apply(self, user: User, item: StockItem):
        now = datetime.datetime.now()
        return now.hour > self.hour and now.minute > self.minute

    def toDAL(self):
        return DalPolicy(self.percent, self.shopname, "simple", self.ID, "isAfterTime", self.hour, self.minute)

    def fromDAL(self, dal: DalPolicy):
        self.__init__(dal.shopname, dal.ID, dal.name, dal.arg1, dal.arg2)