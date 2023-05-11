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
        self.m.adding_item_to_the_shops_stock(self.u, "itemname", "shopname", "category", "description", 5, 10)
        self.m.logout(self.u)

    def testGoodGuest(self):
        r = self.m.info_about_shop_in_the_market_and_his_items_name(self.u, "shopname")
        self.assertEqual(r.res, {'name': 'shopname','founder': 'username','items':[{'name': 'itemname','amount': 10,'category': 'category','description': 'description','price':5.0}],'owners': [],'shopopen': True, 'managers': []}, r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.info_about_item_in_shop(self.u, "itemname", "shopname")
        self.assertTrue(not r.res is None, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testGoodMember(self):  # in case information is defferent
        self.m.login_into_the_trading_system(self.u, "username", "password")
        r = self.m.info_about_shop_in_the_market_and_his_items_name(self.u, "shopname")
        self.assertEqual(r.res, {'name': 'shopname','founder': 'username','items':[{'name': 'itemname','amount': 10,'category': 'category','description': 'description','price':5.0}],'owners': [],'shopopen': True, 'managers': []}, r.res)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.info_about_item_in_shop(self.u, "itemname", "shopname")
        self.assertTrue(not r.res is None, r.exc)
        self.assertTrue((not r.isexc), r.exc)


    def testbadShopGuest(self):
        r = self.m.info_about_shop_in_the_market_and_his_items_name(self.u, "badshopname")
        self.assertTrue(r.isexc, r.exc)


    def testbadShopMember(self):
        self.m.login_into_the_trading_system(self.u, "username", "password")
        r = self.m.info_about_shop_in_the_market_and_his_items_name(self.u, "badshopname")
        self.assertTrue(r.isexc, r.exc)


    def testbadItemGuest(self):
        r = self.m.info_about_item_in_shop(self.u, "baditemname", "shopname")
        self.assertTrue(r.res is None, r.exc)


    def testbadShopMember(self):
        self.m.login_into_the_trading_system(self.u, "username", "password")
        r = self.m.info_about_item_in_shop(self.u, "baditemname", "shopname")
        self.assertEqual(r.res, None, r.res)


if __name__ == '__main__':
    unittest.main()
