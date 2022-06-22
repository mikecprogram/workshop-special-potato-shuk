# from .Logger import Logger
from Dev.DomainLayer.Objects.Shop import Shop


class ShoppingBasket:

    def __init__(self, shoppingCart, shop):
        self.shoppingCart = shoppingCart
        self.shop = shop
        self.stockItems = {}  # {itemname, count}

    def validate_purchase(self, user):
        for name in self.stockItems.keys():
            if not self.shop.validate_purchase(user, name):
                return False
        return True

    def calculate_price(self, user):
        sum = 0
        for itemname in self.stockItems.keys():
            nu = self.shop.calculate_price(user, itemname, self.stockItems[itemname])
            # print(name, nu)
            sum += nu
        return sum

    def raw_price(self):
        sum = 0
        for name, amount in self.stockItems.items():
            sum += self.shop.getItemPrice(name) * amount
        return sum

    def addItem(self, item_name, amount):
        if not (self.shop.itemExists(item_name)):
            raise Exception("No such item found in shop")
        if not (item_name in self.stockItems.keys()):
            self.stockItems[item_name] = 0
        if not (self.shop.isAmount(item_name, self.stockItems[item_name] + amount)):
            raise Exception("No such amount available in shop")
        self.stockItems[item_name] = self.stockItems[item_name] + amount

    def removeItem(self, item_name, amount):
        if not (self.shop.itemExists(item_name)):
            raise Exception("No such item found in shop")
        if self.stockItems[item_name] < amount:
            raise Exception("No such amount available in basket")
        if not (item_name in self.stockItems):
            raise Exception("Item is not even in the basket!")
        if amount == self.stockItems[item_name]:
            del self.stockItems[item_name]
        else:
            self.stockItems[item_name] = self.stockItems[item_name] - amount
        return True

    def checkBasket(self):
        # return self.stockItems
        ret = []
        for name, amount in self.stockItems.items():
            item = self.shop.getItemInfo(name)
            item['count'] = amount
            ret.append(item)
        return ret

    def clear(self):
        self.shoppingCart = None
        self.shop = None
        self.stockItems = None

    def purchase(self, user):
        self.shop.aqcuirePurchaseLock()
        try:
            for name in self.stockItems:
                amount = self.stockItems[name]
                if not (self.shop.isAmount(name, amount)):
                    raise Exception("Not enough left from item %d" % name)
                self.shop.purchase(user, name, amount)

        except Exception as exception:
            self.shop.release_release_lock()
            raise exception
        self.stockItems.clear()
        self.shop.release_release_lock()
        return True

    def to_string(self, customer_token):
        string = "###############################\n"
        string += "Customer token: " + customer_token + "\n"
        string += "Shop name: " + self.shop.getShopName() + "\n"
        string += "Items: \n"
        for item in self.stockItems.values():
            string += item.get_item_report()

        string += "Basket price: " + self.calculate_basket_price() + "\n"

    def calculate_basket_price(self):
        pass  # todo

    def archive(self, token):

        self.shop.archive_shopping_basket(self.to_string(token))

    def is_empty(self):
        return self.stockItems == {}
