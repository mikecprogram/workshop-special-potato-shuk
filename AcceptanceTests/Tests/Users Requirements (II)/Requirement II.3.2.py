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
        self.m.login_into_the_trading_system(self.u,"username","password")


    def testGood(self):
        r = self.m.is_active(self.u)
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        r = self.m.is_member("username")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        self.m.login_into_the_trading_system(self.u,"username","badpassword")
        r = self.m.is_login(self.u)
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        #open a shop
        r = self.m.shop_open(self.u,"shopname")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        r = self.m.info_about_shop_in_the_market_and_his_items_name(self.u,"shopname")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        # logout
        self.m.logout(self.u)
        r = self.m.is_login(self.u)
        self.assertTrue((not r.isexc) and (not r.res))

    def testBad(self):
        r = self.m.is_active(self.u)
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        r = self.m.is_member("username")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        self.m.login_into_the_trading_system(self.u,"username","badpassword")
        r = self.m.is_login(self.u)
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        #open a shop
        r = self.m.shop_open(self.u,"")
        self.assertTrue(r.isexc)
        # logout
        self.m.logout(self.u)
        r = self.m.is_login(self.u)
        self.assertTrue((not r.isexc) and (not r.res))
    
    def testBadDoubleShopName(self):
        r = self.m.is_active(self.u)
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        r = self.m.is_member("username")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        self.m.login_into_the_trading_system(self.u,"username","badpassword")
        r = self.m.is_login(self.u)
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        #open a shop
        r = self.m.shop_open(self.u,"shopname")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        r = self.m.info_about_shop_in_the_market_and_his_items_name(self.u,"shopname")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        r = self.m.shop_open(self.u,"shopname")
        self.assertTrue(r.isexc)
        # logout
        self.m.logout(self.u)
        r = self.m.is_login(self.u)
        self.assertTrue((not r.isexc) and (not r.res))



if __name__ == '__main__':
    unittest.main()
