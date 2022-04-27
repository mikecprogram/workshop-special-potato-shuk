class stockItem:
    def __init__(self,stock,shoppingBasket = None):
        self.stock = stock
        self.discountPolicy = []#load. unsure how to implement (list or singular)
        self.purchasePolicy = []#load
        self.shoppingBasket = shoppingBasket

