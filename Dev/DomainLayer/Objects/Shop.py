from DiscountPolicy import DiscountPolicy
from Logger import Logger
import Stock
import StockItem
import Member
from PurchaseHistory import PurchaseHistory
from Assignment import Assignment


class Shop():

    def __init__(self, shopName: str, founder: Member):
        self._name = shopName
        self._stock = Stock
        self._status = None  # need to confirm if we need shop's status such as closed/open. TODO
        self._founder = founder
        self._owners = {}  # {ownerUsername, Member}
        self._managers = {}  # {managerUsername, Member}
        self._purchasePolicy = []
        self._discountPolicy = DiscountPolicy()
        self._purchaseHistory = PurchaseHistory()
        self._owners_assignments = {}
        self._managers_assignments = {}
        pass

    def add_item(self, item: StockItem):
        self._stock.add(item)

    def remove_item(self, item: StockItem):
        self._stock.remove(item)

    def update_purchase_policy(self):
        pass

    def update_discount_policy(self):
        pass

    def assign_owner(self, assignerUsername, assignee):
        if assignee.get_username() in self._owners:
            raise Exception("Assignee is already an owner of the shop!")
        if self.is_owner(assignerUsername):
            self._owners[assignee.get_username()] = assignee
            self.add_assignment(assignerUsername, assignee.get_username(), self._owners_assignments)
        elif self.is_manager(assignerUsername):
            if self._managers[assignerUsername].can_assign_manager():
                self._owners[assignee.get_username()] = assignee
                self.add_assignment(assignerUsername, assignee.get_username(), self._owners_assignments)
            else:
                raise Exception("Assigner manager does not have the permission to assign owners!")
        else:
            raise Exception("Owner assignment failed!")
        return True

    def assign_manager(self, assignerUsername, assignee):
        if assignee.get_username() in self._managers:
            raise Exception("Assignee is already a manager of the shop!")
        if self.is_owner(assignerUsername):
            self._managers[assignee.get_username()] = assignee
            self.add_assignment(assignerUsername, assignee.get_username(), self._managers_assignments)
        elif self.is_manager(assignerUsername):
            if self._managers[assignerUsername].can_assign_manager():
                self._managers[assignee.get_username()] = assignee
                self.add_assignment(assignerUsername, assignee.get_username(), self._managers_assignments)
            else:
                raise Exception("Assigner manager does not have the permission to assign managers!")
        else:
            raise Exception("Manager assignment failed!")
        return True

    def add_assignment(self, assignerUsername, assigneeUsername, assignment):
        if assignerUsername in assignment:
            assignment[assignerUsername].append(Assignment(assignerUsername, assigneeUsername))
        else:
            assignment[assignerUsername] = [Assignment(assignerUsername, assigneeUsername)]

    def close_shop(self):
        pass  # just change state of shop to closed TODO

    def is_manager(self, managerUsername):
        return managerUsername in self._managers

    def is_owner(self, ownerUsername):
        return self._owners[ownerUsername] is not None or self._founder.get_username() == ownerUsername

    def getTotalDiscount(self, user):
        totaldiscount = 1
        for discount in self._discountPolicy:
            totaldiscount = totaldiscount * discount.getDiscount(user)
        return totaldiscount
