import unittest
import sys
# this is how you import from different folder in python:

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
        self.m.shop_open(self.u, "rockshop")

    def tearDown(self):
        self.m.logout(self.u)

    def testGood(self):  # find all items with empty search
        lst_old = self.m.general_items_searching(self.u)
        # print(lst_old.exception, lst_old.response)
        self.assertTrue(len(lst_old.res) == 0)
        r = self.m.adding_item_to_the_shops_stock(self.u, "itemname1", "shopname", "animal objects", "cats and clocks",
                                                  5, 10)
        self.assertTrue((not r.isexc) and r.res)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "dogs and locks", 2,
                                              50)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname3", "rockshop", "rocks", "rock collection", 1, 5)
        lst_new = self.m.general_items_searching(self.u)
        # print(lst_new.response)
        self.assertTrue(len(lst_old.res) == 0 and len(lst_new.res) == 3)

    def testBad(self):  # cant find items that dont get added
        lst_old = self.m.general_items_searching(self.u)
        self.m.adding_item_to_the_shops_stock(self.u, "a", "shopname", "animal objects", "cats and clocks", -2, 10)
        self.m.adding_item_to_the_shops_stock(self.u, "b", "shopname", "animal objects", "cats and clocks", 5, -10)
        self.m.adding_item_to_the_shops_stock(self.u, "", "shopname", "animal objects", "cats and clocks", 5, 10)
        lst_new = self.m.general_items_searching(self.u)
        self.assertTrue(len(lst_old.res) == 0 and len(lst_new.res) == 0)


if __name__ == '__main__':
    unittest.main()
