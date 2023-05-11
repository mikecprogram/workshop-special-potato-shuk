import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u1 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u2 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u3 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u4 = self.m.get_into_the_Trading_system_as_a_guest().res

        self.m.registration_for_the_trading_system(self.u1, "username1", "password1")
        self.m.registration_for_the_trading_system(self.u2, "username2", "password2")
        self.m.registration_for_the_trading_system(self.u3, "username3", "password3")
        self.m.registration_for_the_trading_system(self.u4, "username4", "password4")
        self.m.login_into_the_trading_system(self.u1, "username1", "password1")
        self.m.login_into_the_trading_system(self.u2, "username2", "password2")
        self.m.login_into_the_trading_system(self.u3, "username3", "password3")
        self.m.login_into_the_trading_system(self.u4, "username4", "password4")

        self.m.shop_open(self.u1, "shopname")

    def tearDown(self):
        self.m.logout(self.u1)
        self.m.logout(self.u2)
        self.m.logout(self.u3)
        self.m.logout(self.u4)

    def testGood(self):
        self.m.shop_owner_assignment(self.u1, "shopname", "username2")
        self.m.shop_owner_assignment(self.u2, "shopname", "username3")
        r1 = self.m.delete_shop_owner(self.u1, "shopname", "username2")
        r2 = self.m.shop_owner_assignment(self.u3, "shopname", "username4")
        # print(r2.exception)
        self.assertTrue((not r1.isexc), r1.exc)
        self.assertTrue((r2.isexc), r2.exc)

    def testBad(self):
        self.m.shop_owner_assignment(self.u1, "shopname", "username2")
        self.m.shop_owner_assignment(self.u2, "shopname", "username3")
        r1 = self.m.delete_shop_owner(self.u3, "shopname", "username1")
        # print(r1.exception)
        self.assertTrue((r1.isexc), r1.exc)


if __name__ == '__main__':
    unittest.main()
