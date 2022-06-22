# from .Logger import Logger
from Dev.DomainLayer.Objects.paymentServiceInterface import paymentServiceInterface


class PaymentService(paymentServiceInterface):

    def __init__(self):
        pass

    def request_payment(self, amount, payment_details):
        return True
