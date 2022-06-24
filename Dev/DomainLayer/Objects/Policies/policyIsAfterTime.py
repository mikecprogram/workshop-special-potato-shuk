from Dev.DomainLayer.Objects import StockItem, User
from Dev.DomainLayer.Objects.Policies.Composable import Composable
import datetime


class policyHasPrice(Composable):

    def __init__(self, ID, percent, hour, minute):
        self.ID = ID
        self.percent = float(percent)
        self.hour = int(hour)
        self.minute = int(minute)

    def apply(self, user: User, item: StockItem):
        now = datetime.datetime.now()
        return now.hour > self.hour and now.minute > self.minute
