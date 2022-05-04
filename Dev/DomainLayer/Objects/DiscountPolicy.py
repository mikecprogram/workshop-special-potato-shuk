from .Logger import Logger


class DiscountPolicy:

    def ___init___(self):
        self._membersItemVsDiscount = None
        self._guestsItemVsDiscount = None
        raise NotImplementedError

    def add_guest_discount(self, itemId, newDiscount):
        raise NotImplementedError

    def update_guest_discount(self, itemId, new_Discount):
        raise NotImplementedError

    def cancel_guest_discount(self,itemId):
        raise NotImplementedError

    def add_member_discount(self, itemId, newDiscount):
        raise NotImplementedError

    def update_member_discount(self, itemId, new_Discount):
        raise NotImplementedError

    def cancel_member_discount(self,itemId):
        raise NotImplementedError


