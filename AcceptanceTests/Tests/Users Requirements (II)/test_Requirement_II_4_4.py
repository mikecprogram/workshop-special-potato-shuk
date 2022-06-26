import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u2 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u3 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u, "username", "password")
        self.m.registration_for_the_trading_system(self.u2, "username2", "password2")
        self.m.registration_for_the_trading_system(self.u3, "username3", "password3")
        # need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.login_into_the_trading_system(self.u2, "username2", "password2")
        self.m.login_into_the_trading_system(self.u3, "username3", "password3")
        self.m.shop_open(self.u, "shopname")

    def tearDown(self):
        self.m.logout(self.u)
        self.m.logout(self.u2)

    def testGood(self):
        r = self.m.get_owned_shops(self.u2)
        self.assertFalse("shopname" in r.res, r.exc)
        r = self.m.shop_owner_assignment(self.u, "shopname", "username2")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_owned_shops(self.u2)
        self.assertTrue("shopname" in r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testOwnerAssign(self):
        r = self.m.get_owned_shops(self.u2)
        self.assertFalse("shopname" in r.res, r.exc)
        r = self.m.shop_owner_assignment(self.u, "shopname", "username2")
        print(r.res, r.exc)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_owned_shops(self.u2)
        self.assertTrue("shopname" in r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)


        r = self.m.get_owned_shops(self.u3)
        self.assertFalse("shopname" in r.res, r.exc)
        r = self.m.shop_owner_assignment(self.u2, "shopname", "username3")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_owned_shops(self.u3)
        self.assertTrue("shopname" in r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testBAD(self):
        r = self.m.get_owned_shops(self.u2)
        self.assertFalse("shopname" in r.res, r.exc)
        r = self.m.shop_owner_assignment(self.u, "shopname", "username2")
        self.assertTrue((not r.isexc), r.exc)
        self.assertTrue(r.res, r.exc)
        r = self.m.get_owned_shops(self.u2)
        self.assertTrue("shopname" in r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_owned_shops(self.u3)
        self.assertFalse("shopname" in r.res, r.exc)
        r = self.m.shop_owner_assignment(self.u2, "shopname", "username3")
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        r = self.m.get_owned_shops(self.u3)
        self.assertTrue("shopname" in r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        #Actual test:
        r = self.m.shop_owner_assignment(self.u3, "shopname", "username")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.shop_owner_assignment(self.u3, "shopname", "username2")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.shop_owner_assignment(self.u3, "shopname", "username3")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.shop_owner_assignment(self.u2, "shopname", "username")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.shop_owner_assignment(self.u2, "shopname", "username2")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.shop_owner_assignment(self.u2, "shopname", "username3")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.shop_owner_assignment(self.u, "shopname", "username")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.shop_owner_assignment(self.u, "shopname", "username2")
        self.assertTrue(r.isexc, r.exc)
        r = self.m.shop_owner_assignment(self.u, "shopname", "username3")
        self.assertTrue(r.isexc, r.exc)


if __name__ == '__main__':
    unittest.main()
