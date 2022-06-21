import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m=SystemService()
        self.m.initialization_of_the_system()
        self.u=self.m.get_into_the_Trading_system_as_a_guest().res
        self.u2=self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u,"username","password")
        self.m.registration_for_the_trading_system(self.u,"username2","password2")
        #need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u,"username","password")
        self.m.login_into_the_trading_system(self.u2,"username2","password2")
        self.m.shop_open(self.u,"shopname")
    def tearDown(self):
        self.m.logout(self.u)
        self.m.logout(self.u2)
        
    def testGood(self):
        r = self.m.shop_manager_assignment(self.u,"shopname","username2")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        r = self.m.shop_manager_permissions_check(self.u,"username2","shopname")
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        r = self.m.shop_manager_permissions_add(self.u,"username2",1,"shopname")

    def happyCase(self):
        pass

    def sadCase(self):
        pass

    def badCase(self):
        pass


if __name__ == '__main__':
    unittest.main()
