class externalSystems:
    def __init__(self, market):
        self.market = market
        self.paymentSystem = paymentSystem(self)
        self.deliverySystem = deliverySystem(self)
