import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')
from SystemService import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=SystemService()
        self.u=self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u,"username","password")
        #need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.m.shop_open(self.u,"shopname")
        self.m.adding_item_to_the_shops_stock(self.u,"itemname","shopname","category","description",5,10)
        self.m.logout(self.u)
        
               
    def testGoodGuest(self):
        r=self.m.info_about_shop_in_the_market_and_his_items_name(self.u,"shopname")      
        self.assertTrue((not r.isexc) and r.res == ["Shop name: shopname\nFounder: username\n", ["itemname"]])
        r=self.m.info_about_item_in_shop(self.u,"itemname","shopname")
        self.assertTrue((not r.isexc) and not r.res is None)
        
    def testGoodMember(self): #in case information is defferent
        self.m.login_into_the_trading_system(self.u,"username","password")
        r=self.m.info_about_shop_in_the_market_and_his_items_name(self.u,"shopname")
        self.assertTrue((not r.isexc) and r.res == ["Shop name: shopname\nFounder: username\n", ["itemname"]])
        r=self.m.info_about_item_in_shop(self.u,"itemname","shopname")
        self.assertTrue((not r.isexc) and not r.res is None)
        
    def testbadShopGuest(self):
        r=self.m.info_about_shop_in_the_market_and_his_items_name(self.u,"badshopname")
        self.assertTrue(r.isexc)
        
    def testbadShopMember(self):
        self.m.login_into_the_trading_system(self.u,"username","password")
        r=self.m.info_about_shop_in_the_market_and_his_items_name(self.u,"badshopname")
        self.assertTrue(r.isexc)
        
    def testbadItemGuest(self):
        r=self.m.info_about_item_in_shop(self.u,"baditemname","shopname")
        self.assertTrue((not r.isexc) and r.res == None)
        
    def testbadShopMember(self):
        self.m.login_into_the_trading_system(self.u,"username","password")
        r=self.m.info_about_item_in_shop(self.u,"baditemname","shopname")
        self.assertTrue((not r.isexc) and r.res == None)
    
        
if __name__ == '__main__':
    unittest.main()
