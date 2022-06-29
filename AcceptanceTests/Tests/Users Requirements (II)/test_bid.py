import unittest
import sys

from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u2 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u, "username", "password")
        self.m.registration_for_the_trading_system(self.u2, "ownername", "password")
        # need to login, create shop and add items to it for test

        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.shop_open(self.u, "shopname")
        r = self.m.shop_owner_assignment(self.u,"shopname", "ownername")
        self.m.shop_open(self.u, "rockshop")
        self.m.adding_item_to_the_shops_stock(self.u, "itemname1", "shopname", "animal objects", "cats and clocks", 5,
                                              30)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "dogs and locks", 2,
                                              50)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname3", "rockshop", "rocks", "rock collection", 1, 5)

    def testAddBid(self):
        r = self.m.bid_shop_item(self.u, "shopname", "itemname1", 5, 20)
        self.assertTrue((not r.isexc), r.exc)
        self.assertTrue(r.res, r.exc)
        r = self.m.get_bids(self.u, "shopname")
        self.assertTrue((not r.isexc), r.exc)
        self.assertEqual({1: ['shopname', 'username', 'itemname1', 5, 20]},r.res)

        self.m.logout(self.u)
        self.m.login_into_the_trading_system(self.u2, "ownername", "password")
        r = self.m.get_bids(self.u, "shopname")
        self.assertTrue((not r.isexc), r.exc)
        self.assertEqual({1: ['shopname', 'username', 'itemname1', 5, 20]}, r.res)

        r = self.m.accept_bid(self.u2, "shopname", 1)
        self.assertTrue((not r.isexc), r.exc)
        self.assertTrue(r.res, r.exc)

        r = self.m.get_bids(self.u2, "shopname")
        self.assertTrue((not r.isexc), r.exc)
        self.assertEqual({1: ['shopname', 'username', 'itemname1', 5, 20]}, r.res)

        self.m.logout(self.u)
        self.m.login_into_the_trading_system(self.u, "username", "password")
        r = self.m.pay_bid(self.u, 1)
        self.assertTrue((not r.isexc), r.exc)
        self.assertTrue(r.res, r.exc)

        r = self.m.get_bids(self.u, "shopname")
        self.assertTrue((not r.isexc), r.exc)
        self.assertEqual({}, r.res)


if __name__ == '__main__':
    unittest.main()
