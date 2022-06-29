##from .Logger import Logger


class PaymentSystemController():

    def __init__(self,is_demo:bool ):
        self._user = user  # is it necessary here ? answer: ?

    def handshake(self):
        pass
    def pay(self, card_number, month, year, holder, ccv, id,amount):
        pass
    #returns transaction id
    def cancel_pay(self, transaction_id):
        pass#Output: 1 if the cancelation has been successful or -1 if the cancelation has failed.

##from .Logger import Logger

class SupplyingSystemController():

    def __init__(self, user):
        self._user = user  # is it necessary here ? answer: ?

    def handshake(self):
        pass

    def pay(self, card_number, month, year, holder, ccv, id, amount):
        pass

    # returns transaction id
    def cancel_pay(self, transaction_id):
        pass  # Output: 1 if the cancelation has been successful or -1 if the cancelation has failed.