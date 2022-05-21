from .Logger import Logger
import time

class DiscountPolicy:

    def ___init___(self,isGuestOnly,isMemberOnly,discount,mustBuyItemsID,endDate,cuponCode):
        self._isGuestOnly = isGuestOnly
        self._isMemberOnly = isMemberOnly
        self._discount = discount
        self._mustBuyItemsID = mustBuyItemsID
        self._endDate = endDate
        self._cuponCode = cuponCode
        
    def setDiscount(self,discount):#20% off is 0.2 for example
        self._discount = discount

    def setIsGuestOnly(self,isGuestOnly):
        self._isGuestOnly = isGuestOnly
    def setIsMemberOnly(self,isMemberOnly):
        self._isMemberOnly = isMemberOnly
    def setMustBuyItemsID(self, mustBuyItemsID):
        self._mustBuyItemsID = mustBuyItemsID

    def userHaveItems(self,user):
        if len(self._mustBuyItemsID) > 0:
            userItemsID = (item.getID() for item in user.getAllItems())
            return all( (itemID in userItemsID) for itemID in self._mustBuyItemsID)
        return True
    def getDiscount(self,user,cupons):
        if (self._isGuestOnly & (not(type(self._state).__name__ == "Guest"))) :
            return 1
        
        if (self._isMemberOnly & (not(type(self._state).__name__ == "Member"))) :
            return 1
        if not(self.userHaveItems(user)) :
            return 1
        if self._endDate < time.time():
            return 1
        if self._cuponCode != None:
            if not(self._cuponCode in cupons):
                return 1

        return self._discount



