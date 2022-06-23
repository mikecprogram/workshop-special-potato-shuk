import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u1 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u2 = self.m.get_into_the_Trading_system_as_a_guest().res

        self.m.registration_for_the_trading_system(self.u, "username", "password")
        # need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.login_into_the_trading_system(self.u1, "Alex", "Alex_123456")
        self.m.shop_open(self.u, "shopname")

        self.u2 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u2, "username2", "password2")
        self.m.login_into_the_trading_system(self.u2, "username2", "password2")
        self.m.adding_item_to_the_shops_stock(self.u, "itemname1", "shopname", "animal objects", "cats and clocks", 5,
                                              10)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "dogs and locks", 2,
                                              50)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname3", "rockshop", "rocks", "rock collection", 1, 5)
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 1)

    def tearDown(self):
        self.m.logout(self.u)

    def testGood(self):
        r = self.m.in_shop_purchases_history_request(self.u,"shopname")
        self.assertEqual(r.res,"", r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.in_shop_purchases_history_request(self.u2,"shopname")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.in_shop_purchases_history_request(self.u1,"shopname")
        self.assertEqual(r.res,"", r.exc)
        self.assertTrue((not r.isexc), r.exc)

        price = self.m.calculate_cart_price(self.u).res
        r = self.m.Shopping_cart_purchase(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")
        self.assertEqual(r.res, "User '%s' bought %d of %s for %f.\n"%("username",1,"itemname1",price), r.res)
        self.assertTrue((not r.isexc), r.exc)

        r = self.m.in_shop_purchases_history_request(self.u1, "shopname")
        self.assertEqual(r.res, "User '%s' bought %d of %s for %f.\n"%("username",1,"itemname1",price), r.res)
        self.assertTrue((not r.isexc), r.exc)

        r = self.m.in_shop_purchases_history_request(self.u2,"shopname")
        self.assertTrue(r.isexc, r.exc)

    def happyCase(self):
        pass

    def sadCase(self):
        pass

    def badCase(self):
        pass


if __name__ == '__main__':
    unittest.main()
