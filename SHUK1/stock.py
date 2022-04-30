from asyncio.windows_events import NULL
from re import I
from SHUK1.stockItem import stockItem


class stock:
    def __init__(self,shop):
        self.shop = shop
        self.stockItems = []#load

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

    def search(self,itemName,category,keyword,maxPrice,minItemRating,minShopRating):
        print("need to implement search in stock")
        return []
    
    def checkPurchase(self, itemName, itemNumber ,user):

        print("need to implement checkPurchase in stock")

        return True
    
