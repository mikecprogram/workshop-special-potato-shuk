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
        self.m.adding_item_to_the_shops_stock(self.u, "itemname1", "shopname", "animal objects", "cats and clocks", 5,
                                              10)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "dogs and locks", 2,
                                              50)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname3", "rockshop", "rocks", "rock collection", 1, 5)

    def testPurchase(self):
        self.m.logout(self.u)
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.Shopping_cart_purchase(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testAddedAsMember(self):
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 1)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        self.m.logout(self.u)
        r = self.m.Shopping_cart_purchase(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)


if __name__ == '__main__':
    unittest.main()
