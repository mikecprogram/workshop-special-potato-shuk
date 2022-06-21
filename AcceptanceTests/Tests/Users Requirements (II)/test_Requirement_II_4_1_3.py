import unittest
import sys

from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m=SystemService()
        self.m.initialization_of_the_system()
        self.u=self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u,"username","password")
        #need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.m.shop_open(self.u,"shopname")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        #lst_old = self.m.general_items_searching(self.u)

    def tearDown(self):
        self.m.logout(self.u)
        
    def testGood(self):
        lst_old = self.m.general_items_searching(self.u,item_keyword="clocks")
        self.m.change_items_details_in_shops_stock(self.u,"itemname1","shopname",item_desc="AAA")
        lst_new = self.m.general_items_searching(self.u,item_keyword="clocks")
        self.assertTrue(len(lst_old.res) == 1 and len(lst_new.res) == 0,r.exc)

    def testBadName(self):
        lst_old = self.m.general_items_searching(self.u,item_keyword="clocks")
        self.m.change_items_details_in_shops_stock(self.u,"itemname1","shopname",new_name="")
        lst_new = self.m.general_items_searching(self.u,item_keyword="clocks")
        self.assertTrue(len(lst_old.res) == 1 and len(lst_new.res) == 1,r.exc)

    def testBadPrice(self):
        lst_old = self.m.general_items_searching(self.u,item_keyword="clocks")
        self.m.change_items_details_in_shops_stock(self.u,"itemname1","shopname",item_price=-10)
        lst_new = self.m.general_items_searching(self.u,item_keyword="clocks")
        self.assertTrue(len(lst_old.res) == 1 and len(lst_new.res) == 1,r.exc)

        
if __name__ == '__main__':
    unittest.main()
