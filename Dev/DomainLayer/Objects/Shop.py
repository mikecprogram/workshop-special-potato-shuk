from .Logger import Logger
import Stock
import StockItem
import Member
import PurchasePolicy
import DiscountPolicy
import PurchaseHistory
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

    def assign_owner(self, assigner, assignee):
        if assignee not in self._owners:
            self._owners.append(assignee)
            self._assignments[assigner].append(Assignment(assigner, assignee))

    def assign_manager(self, assignerUsername, assignee):
        if self.is_owner(assignerUsername):
            self._managers[assignerUsername] = assignee
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
        if assignment[assignerUsername] is not None:
            assignment[assignerUsername].append(Assignment(assignerUsername, assigneeUsername))
        else:
            assignment[assignerUsername] = [Assignment(assignerUsername, assigneeUsername)]

    def close_shop(self):
        pass  # just change state of shop to closed TODO

    def is_manager(self, managerUsername):
        return self._managers[managerUsername] is not None

    def is_owner(self, ownerUsername):
        return self._owners[ownerUsername] is not None or self._founder.get_username() == ownerUsername

    def getTotalDiscount(self, user):
        totaldiscount = 1
        for discount in self._discountPolicy:
            totaldiscount = totaldiscount * discount.getDiscount(user)
        return totaldiscount
