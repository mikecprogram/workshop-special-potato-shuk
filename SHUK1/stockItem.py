class stockItem:
    def __init__(self,stock, name, desc, id, price, rating,category,shoppingBasket = None):
        self.stock = stock
        self.discountPolicy = []#load. unsure how to implement (list or singular)
        self.purchasePolicy = []#load
        self.shoppingBasket = shoppingBasket
        self.name = name
        self.itemDescription = desc
        self.id = id
        self.price = price
        self.category = category
        self.rating = rating

    def changeItemDescription(self,description):
        self.itemDescription = description

    def printItem(self):
        print("Name: " + self.name + " ,ID:" + self.id)
        print("Description:" + self.itemDescription)