from .Logger import Logger
from PaymentService import PaymentService


class ExternalServices:

    def __init__(self):
        self._paymentService = None
        self._shippingService = PaymentService()
        pass

    def execute_payment(self):
        self._paymentService.request_payment()





