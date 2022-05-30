#from .Logger import Logger
from Dev.DomainLayer.Objects.shippingServiceInterface import shippingServiceInterface

class ShippingService(shippingServiceInterface):

    def __init__(self):
        pass
    
    def requestShipping(self):
        return True