##from .Logger import Logger
import time


class DiscountPolicy(db.Entity):
        self._isGuestOnly = isGuestOnly
        self._isMemberOnly = isMemberOnly
        self._discount = discount
        self._mustBuyItemsID = mustBuyItemsID
        self._endDate = endDate
        self._cuponCode = cuponCode
