from asyncio.windows_events import NULL
from re import I
from SHUK1.stockItem import stockItem


class stock:
    def __init__(self,shop):
        self.shop = shop
        self.stockItems = [] #  , load

    def addItemToStock(self,item : stockItem, stockNumber):
        flag = False
        for i in self.stockItems:
            if i[0].id == item.id:
                flag = True
                break
        if flag == False:
            self.stockItems.append((item,stockNumber))
        else:
            print("The item is already on the store stock," + item.printItem())

    def removeItemFromStock(self,item : stockItem):
        self.removeItemFromStock(itemID= item.id)

    def removeItemFromStock(self,itemID):
        tmp = NULL
        for i in self.stockItems:
            if i[0].id == itemID:
                tmp = i
                break
        if tmp != NULL:
            self.stockItems.remove(tmp)
        else:
            print("The item is'nt on the store stock, can't remove it!")

    def search(self,itemName,category,minItemRating,maxItemRating,minPrice,maxPrice):
        ret = []
        for i in self.stockItems:
            if itemName in i[0].name:
                ret.append(i)
                pass
            if category in i[0].category:
                ret.append(i)
                pass
            if minItemRating>=0 or maxItemRating>=0:
                if i[0].rating>=minItemRating>=0 or maxItemRating==-1:
                    ret.append(i)
                    pass
                if maxItemRating>= i[0].rating >=0 or minItemRating==-1:
                    ret.append(i)
                    pass
                if minItemRating <= i[0].rating <= maxItemRating:
                    ret.append(i)
                    pass
            if minPrice>=0 or maxPrice>=0:
                if i[0].price>=minPrice>=0 or maxPrice==-1:
                    ret.append(i)
                    pass
                if maxPrice>= i[0].price >=0 or minPrice==-1:
                    ret.append(i)
                    pass
                if minPrice <= i[0].price <= maxPrice:
                    ret.append(i)
                    pass
        return ret
    
    def checkPurchase(self, itemName, itemNumber ,user):

        print("need to implement checkPurchase in stock")

        return True