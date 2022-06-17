from paymentSystem import *
from deliverySystem import *
class externalSystems:
    def __init__(self, market):
        self.market = market
        self.paymentSystem = paymentSystem(self)
        self.deliverySystem = deliverySystem(self)

    def checkDelivery(self, user):
        print("need to implement checkDelivery in externalSystems")
        return True

    def makeDelivery(self, user):
        print("need to implement makeDelivery in externalSystems")
        return True

    def makePayment(self, price , user):
        print("need to implement makePayment in externalSystems")
        return True
