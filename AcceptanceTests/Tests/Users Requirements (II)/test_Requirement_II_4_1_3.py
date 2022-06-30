import unittest
import sys

from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u, "username", "password")
        self.u1 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u1, "username1", "password1")
        self.u2 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u2, "username2", "password2")
        # need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.login_into_the_trading_system(self.u1, "username1", "password1")
        self.m.login_into_the_trading_system(self.u2, "username2", "password2")
        self.m.shop_open(self.u, "shopname")
        self.m.shop_manager_assignment(self.u, "shopname","username1")
        self.m.shop_manager_permissions_delete(self.u, "username1", 1,"shopname")
        self.m.shop_open(self.u1, "shopname1")
        self.m.adding_item_to_the_shops_stock(self.u, "itemname1", "shopname", "animal objects", "cats and clocks", 5,
                                              10)
        # lst_old = self.m.general_items_searching(self.u)

    def tearDown(self):
        self.m.logout(self.u)

    def testGood(self):
        lst_old = self.m.general_items_searching(self.u, item_keyword="clocks")
        self.m.change_items_details_in_shops_stock(self.u, "itemname1", "shopname", item_desc="AAA")
        lst_new = self.m.general_items_searching(self.u, item_keyword="clocks")
        diffcountofitems = sum([len(result) for result in lst_new.res.values()])
        self.assertEqual(diffcountofitems, 0, lst_new.res)
        diffcountofitems = sum([len(result) for result in lst_old.res.values()])
        self.assertEqual(diffcountofitems, 1, lst_old.res)

    def testBadName(self):
        lst_old = self.m.general_items_searching(self.u, item_keyword="clocks")
        self.m.change_items_details_in_shops_stock(self.u, "itemname1", "shopname", new_name="")
        lst_new = self.m.general_items_searching(self.u, item_keyword="clocks")
        diffcountofitems = sum([len(result) for result in lst_new.res.values()])
        self.assertEqual(diffcountofitems, 1, lst_new.res)
        diffcountofitems = sum([len(result) for result in lst_old.res.values()])
        self.assertEqual(diffcountofitems, 1, lst_old.res)

    def testBadPrice(self):
        lst_old = self.m.general_items_searching(self.u, item_keyword="clocks")
        self.m.change_items_details_in_shops_stock(self.u, "itemname1", "shopname", item_price=-10)
        lst_new = self.m.general_items_searching(self.u, item_keyword="clocks")
        diffcountofitems = sum([len(result) for result in lst_new.res.values()])
        self.assertEqual(diffcountofitems, 1, lst_new.res)
        diffcountofitems = sum([len(result) for result in lst_old.res.values()])
        self.assertEqual(diffcountofitems, 1, lst_old.res)

    def testHaveNoPermission(self):
        lst_old = self.m.general_items_searching(self.u, item_keyword="clocks")
        self.m.change_items_details_in_shops_stock(self.u, "itemname1", "shopname", new_name="")
        lst_new = self.m.general_items_searching(self.u, item_keyword="clocks")
        diffcountofitems = sum([len(result) for result in lst_new.res.values()])
        self.assertEqual(diffcountofitems, 1, lst_new.res)
        diffcountofitems = sum([len(result) for result in lst_old.res.values()])
        self.assertEqual(diffcountofitems, 1, lst_old.res)


if __name__ == '__main__':
    unittest.main()
