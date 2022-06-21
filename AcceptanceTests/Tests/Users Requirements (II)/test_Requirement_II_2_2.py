import unittest
import sys
# this is how you import from different folder in python:
# sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')
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
        self.m.adding_item_to_the_shops_stock(self.u, "itemname1", "shopname", "animal objects", "cats and clocks", 5,
                                              10)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname2", "shopname", "animal objects", "dogs and locks", 2,
                                              50)
        self.m.adding_item_to_the_shops_stock(self.u, "itemname3", "rockshop", "rocks", "rock collection", 1, 5)
        self.m.logout(self.u)

    def testSearchName(self):
        r = self.m.general_items_searching(self.u, item_name="itemname1")

        self.assertEqual(r.res, [["shopname", "itemname1"]], , r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchCategory(self):
        r = self.m.general_items_searching(self.u, category="animal objects")
        self.assertEqual(r.res, [["shopname", "itemname1"], ["shopname", "itemname2"]], , r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchKeyword(self):
        r = self.m.general_items_searching(self.u, item_keyword="cats")
        # print(r.exception,r.response)
        self.assertEqual(r.res, [["shopname", "itemname1"]], , r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchMaxPrice(self):
        r = self.m.general_items_searching(self.u, item_maxPrice=3)
        # print(r.exception,r.response)
        self.assertEqual(r.res, [["shopname", "itemname2"], ["rockshop", "itemname3"]], , r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchAll(self):
        r = self.m.general_items_searching(self.u, item_name="itemname2", category="animal objects",
                                           item_keyword="dogs", item_maxPrice=3)
        # print(r.exception,r.response)
        self.assertEqual(r.res, [["shopname", "itemname2"]], , r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchBad(self):
        r = self.m.general_items_searching(self.u, item_name="itemname42")
        self.assertEqual(r.res, [], , r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchAny(self):
        r = self.m.general_items_searching(self.u)
        self.assertTrue(r.res == [['shopname', 'itemname1'], ['shopname', 'itemname2'], ['rockshop', 'itemname3']],
                        r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchExclusive(self):
        r = self.m.general_items_searching(self.u, category="animal objects", item_maxPrice=1)
        self.assertEqual(r.res, [], , r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchPartialDesc(self):
        r = self.m.general_items_searching(self.u, item_keyword="ock")
        self.assertTrue(r.res == [["shopname", "itemname1"], ["shopname", "itemname2"], ["rockshop", "itemname3"]],
                        r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchPartialName(self):
        r = self.m.general_items_searching(self.u, item_keyword="ocks")
        self.assertTrue(r.res == [["shopname", "itemname1"], ["shopname", "itemname2"], ["rockshop", "itemname3"]],
                        r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testSearchWhitespace(self):
        r = self.m.general_items_searching(self.u, item_keyword="ock ")
        self.assertEqual(r.res, [["rockshop", "itemname3"]], , r.res)
        self.assertTrue((not r.isexc), r.exc)


if __name__ == '__main__':
    unittest.main()
