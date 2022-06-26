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
        r = self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 1)

    def testPurchaseHistory(self):
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")
        self.assertTrue((not r.isexc), r.exc)
        self.assertEqual(r.res, "", r.res)
        price = self.m.calculate_cart_price(self.u).res
        r = self.m.Shopping_cart_purchase(self.u)

        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")#WTF why usage of username instead of token?
        self.assertEqual(r.res, "User '%s' bought %d of %s for %f.\n"%("username",1,"itemname1",price), r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testAfterRelog(self):
        self.m.logout(self.u)
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")
        self.assertTrue(r.isexc, r.exc)
        self.m.login_into_the_trading_system(self.u, "username", "password")
        price = self.m.calculate_cart_price(self.u).res
        r = self.m.Shopping_cart_purchase(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")
        print(r.res, r.exc)
        self.assertEqual(r.res, "User '%s' bought %d of %s for %f.\n"%("username",1,"itemname1",price), r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testAddedAsGuest(self):
        r = self.m.logout(self.u)
        r = self.m.in_shop_purchases_history_request(self.u,"shopname")
        self.assertTrue(r.isexc, r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname1", "shopname", 1)
        price = self.m.calculate_cart_price(self.u).res
        r = self.m.Shopping_cart_purchase(self.u)
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.in_shop_purchases_history_request(self.u,"shopname")
        self.assertEqual(r.res, "User '%s' bought %d of %s for %f.\n"%("Guest",1,"itemname1",price), r.res)
        self.assertTrue(not r.isexc, r.exc)

    def testMultiAdd(self):
        price1 = self.m.calculate_cart_price(self.u).res
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")
        self.assertEqual(r.res, "", r.res)
        self.assertTrue((not r.isexc), r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 2)
        price2 = self.m.calculate_item_price(self.u, "shopname","itemname2").res
        self.m.login_into_the_trading_system(self.u, "username", "password")
        r = self.m.Shopping_cart_purchase(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")
        checkstring = ("User '%s' bought %d of %s for %f.\n"%("username",1,"itemname1",price1)) +("User '%s' bought %d of %s for %f.\n"%("username",2,"itemname2",price2))
        self.assertEqual(r.res,checkstring , r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testMultiPurchase(self):
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")
        self.assertEqual(r.res, "", r.res)
        self.m.logout(self.u)
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")
        self.assertTrue( r.isexc, r.exc)
        self.m.shopping_carts_add_item(self.u, "itemname2", "shopname", 2)
        price2 = self.m.calculate_item_price(self.u, "shopname","itemname2").res
        checkstring = ("User '%s' bought %d of %s for %f.\n" % ("Guest", 2, "itemname2", price2))

        r = self.m.Shopping_cart_purchase(self.u)
        self.assertTrue((not r.isexc), r.exc)
        self.m.login_into_the_trading_system(self.u, "username", "password")
        price1 = self.m.calculate_item_price(self.u, "shopname","itemname1").res
        r = self.m.Shopping_cart_purchase(self.u)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.in_shop_purchases_history_request(self.u, "shopname")
        checkstring += ("User '%s' bought %d of %s for %f.\n" % ("username", 1, "itemname1", price1))
        self.assertEqual(r.res,checkstring, r.res)
        self.assertTrue((not r.isexc), r.exc)


if __name__ == '__main__':
    unittest.main()
