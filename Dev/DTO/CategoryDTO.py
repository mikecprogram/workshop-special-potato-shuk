class CategoryDTO:

    def __init__(self,shop, catagoryName, catagoryId,stockItems):
        self.shop = shop
        self.catagoryName = catagoryName
        self.catagoryId = catagoryId
        #self.purchasePolicy = []
        #self.discountPolicy = []
        self.stockItems = stockItems
