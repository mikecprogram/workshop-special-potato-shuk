import unittest
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
    def tearDown(self):
        self.m.logout(self.u)
        
    def testGood(self):
        r = self.m.in_shop_purchases_history_request(self.u)
        self.assertTrue((not r.isexc) and r.res)


    def happyCase(self):
        pass

    def sadCase(self):
        pass

    def badCase(self):
        pass


if __name__ == '__main__':
    unittest.main()
