from Dev.DomainLayer.Objects.Policies.policyIsShop import policyIsShop
from Dev.DomainLayer.Objects.StockItem import *
from Dev.DomainLayer.Objects.Assignment import Assignment
from Dev.DomainLayer.Objects.Stock import Stock
from Dev.DomainLayer.Objects.PurchaseHistory import PurchaseHistory
import threading


class ShopDTO:

    def __init__(self, shop_name: str,stock,is_open,founder,owners,/
                 ,managers,owners_assignments,managers_assignments,purchases_history,notificationPlugin):
        self.name = shop_name
        self.stock = stock
        self.is_open = is_open  # need to confirm if we need shop's status such as closed/open. TODO
        self.founder = founder
        self.owners = owners  # {ownerUsername, Member} (ò_ó)!!!!!!!!!!!!!!!!!
        self.managers = managers  # {managerUsername, Member}
        #self.purchasePolicies = purchasePolicies
        #self.discountPolicies = discountPolicies
        self.owners_assignments = owners_assignments
        self.managers_assignments = managers_assignments
        self.purchases_history = purchases_history
        self.notificationPlugin = notificationPlugin

