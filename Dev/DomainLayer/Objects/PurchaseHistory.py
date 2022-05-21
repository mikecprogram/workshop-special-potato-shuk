from .Logger import Logger


class PurchaseHistory:

    def ___init___(self):
        self.purchaseString = ""#load
        pass
        
    def append(self,data):
        self.purchaseString = self.purchaseString + data + "\n"
        
