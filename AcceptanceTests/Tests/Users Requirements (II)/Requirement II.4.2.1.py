import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().response
        self.m.registration_for_the_trading_system(self.u, "username", "password")
        # need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.shop_open(self.u, "shopname")
        self.m.adding_item_to_the_shops_stock(self.u, "itemname", "shopname", "animal objects", "cats and clocks", 5,10)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "bird bricks", 2, 50)

    def testHasAmountPurchase(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        print(r.exception, r.response)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasAmount", "itemname", 4, 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1]])

    def testIsShopPurchase(self):
        r = self.m.add_policy(self.u, 10, "isShop")
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "isShop", 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1]])

    def testHasRawPricePurchase(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", 4)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.is_exception) and r.response == [[1, "hasPrice", 4, 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.is_exception) and r.response)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1]])
        r = self.m.get_item_policies(self.u, "shopname", "itemname")
        self.assertTrue((not r.is_exception) and r.response == [["purchase", 1]])

if __name__ == '__main__':
    unittest.main()
