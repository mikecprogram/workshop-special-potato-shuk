# from .Logger import Logger


class PurchaseHistory():

    def __init__(self):
        self.purchaseString = ""  # load
        pass

    def append(self, data):
        self.purchaseString = self.purchaseString + data + "\n"

    def get_string(self):
        return self.purchaseString
