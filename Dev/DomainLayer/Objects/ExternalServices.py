# from .Logger import Logger
from Dev.DomainLayer.Objects.paymentServiceInterface import paymentServiceInterface
from Dev.DomainLayer.Objects.shippingServiceInterface import shippingServiceInterface


class ExternalServices:

    def __init__(self, payment_service: paymentServiceInterface, shipping_service: shippingServiceInterface):
        self._paymentService = payment_service
        self._paymentService.handshake()
        self._shippingService = shipping_service
        self._shippingService.handshake()

    def execute_payment(self, card_number, month, year, holder, ccv, id):
        return self._paymentService.pay(card_number, month, year, holder, ccv, id)

    def cancel_payment(self, transaction_id):
        return self._paymentService.cancel_pay(transaction_id)
        # Output: 1 if the cancelation has been successful or -1 if the cancelation has failed.

    def execute_shipment(self, name, address, city, country, zip):
        return self._shippingService.supply(name, address, city, country, zip)
        # Output: transaction id - an integer in the range [10000, 100000] which indicates a
        # transaction number if the transaction succeeds or -1 if the transaction has failed.

    def cancel_shipment(self, transaction_id):
        return self._shippingService.cancel_supply(transaction_id)
        # Output: 1 if the cancelation has been successful or -1 if the cancelation has failed.
