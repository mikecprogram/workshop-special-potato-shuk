from .Logger import Logger
from PaymentService import PaymentService
from ShippingService import ShippingService


class ExternalServices:

    def __init__(self):
        self._paymentService = PaymentService()
        self._shippingService = ShippingService()
        pass

    def execute_payment(self):
        self._paymentService.request_payment()

    def execute_shipment(self):
        self._shippingService.requestShipping()
