#from .Logger import Logger
from paymentServiceInterface import paymentServiceInterface
from shippingServiceInterface import shippingServiceInterface


class ExternalServices:

    def __init__(self,PaymentService : paymentServiceInterface, ShippingService : shippingServiceInterface):
        self._paymentService = PaymentService
        self._shippingService = ShippingService

    def execute_payment(self):
        self._paymentService.request_payment()

    def execute_shipment(self):
        self._shippingService.requestShipping()
