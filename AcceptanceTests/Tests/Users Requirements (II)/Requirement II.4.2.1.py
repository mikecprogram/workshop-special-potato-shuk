import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u, "username", "password")
        # need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.shop_open(self.u, "shopname")
        self.m.adding_item_to_the_shops_stock(self.u, "itemname", "shopname", "animal objects", "cats and clocks", 5,10)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "bird bricks", 2, 50)

    def testHasAmountPurchase(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname", 4)
        self.assertTrue((not r.isexc) and r.res)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.isexc) and r.res == [[1, "hasAmount", "itemname", 4, 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.isexc) and r.res)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.isexc) and r.res == [["purchase", 1]])

    def testIsShopPurchase(self):
        r = self.m.add_policy(self.u, 10, "isShop")
        self.assertTrue((not r.isexc) and r.res)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.isexc) and r.res == [[1, "isShop", 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.isexc) and r.res)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.isexc) and r.res == [["purchase", 1]])

    def testHasRawPricePurchase(self):
        r = self.m.add_policy(self.u, 10, "hasPrice", "itemname", 4)
        self.assertTrue((not r.isexc) and r.res)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.isexc) and r.res == [[1, "hasPrice", "itemname", 4, 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "shopname", 1)
        self.assertTrue((not r.isexc) and r.res)
        r = self.m.get_shop_policies(self.u, "shopname")
        self.assertTrue((not r.isexc) and r.res == [["purchase", 1]])

    def testBadShop(self):
        r = self.m.add_policy(self.u, 10, "hasAmount", "itemname", 4)
        self.assertTrue((not r.isexc) and r.res)
        r = self.m.get_my_policies(self.u)
        self.assertTrue((not r.isexc) and r.res == [[1, "hasAmount", "itemname", 4, 10]])
        r = self.m.add_purchase_policy_to_shop(self.u, "badshopname", 1)
        self.assertTrue(r.isexc)

if __name__ == '__main__':
    unittest.main()
