class CategoryDTO:

    def __init__(self,shop= None, catagoryName= None, catagoryId= None,stockItems= None):
        self.shop = shop
        self.catagoryName = catagoryName
        self.catagoryId = catagoryId
        #self.purchasePolicy = []
        #self.discountPolicy = []
        self.stockItems = stockItems
