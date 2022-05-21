from hashlib import new
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
        self.m.adding_item_to_the_shops_stock(self.u,"itemname1","shopname","animal objects","cats and clocks",5,10)
    def tearDown(self):
        self.m.logout(self.u)
        
    def testGood(self):
        lst_old = self.m.general_items_searching(self.u)
        self.m.change_items_details_in_shops_stock(self.u,"itemname1","shopname","")
        lst_new = self.m.general_items_searching(self.u,item_name="itemname1")
        self.assertTrue(lst_old.response[0].des != 0 and lst_new.response[0].des)
if __name__ == '__main__':
    unittest.main()
