import unittest
import sys
from SHUK1.stock import stock
from SHUK1.stockItem import stockItem
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\SHUK1')

from SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m=SystemService()
        self.u=self.m.get_into_the_Trading_system_as_a_guest()
        self.m.registration_for_the_trading_system(self.u,"username","password")
        #need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.m.shop_open(self.u,"shopname")
    def tearDown(self):
        self.m.logout(self.u)
        
    def testGood(self):
        lst_old = self.m.general_items_searching(self.u)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.deleting_item_from_shop_stock(self.u,"itemname1","shopname",10)
        lst_new = self.m.general_items_searching(self.u)
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 0)
    def testGood2(self):
        lst_old = self.m.general_items_searching(self.u)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.deleting_item_from_shop_stock(self.u,"itemname1","shopname",9)
        lst_new = self.m.general_items_searching(self.u)
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 1)
        

    def testBad(self):
        lst_old = self.m.general_items_searching(self.u)
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
        self.m.deleting_item_from_shop_stock(self.u,"itemnamea","shopname",9)
        lst_new = self.m.general_items_searching(self.u)
        self.assertTrue(lst_old.response.count == 0 and lst_new.response.count == 1)


if __name__ == '__main__':
    unittest.main()
