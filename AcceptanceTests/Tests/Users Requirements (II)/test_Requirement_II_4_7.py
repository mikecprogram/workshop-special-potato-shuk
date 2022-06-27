import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u2 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.u3 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u, "username", "password")#founder
        self.m.registration_for_the_trading_system(self.u2, "username2", "password2")#owner
        self.m.registration_for_the_trading_system(self.u3, "username3", "password3")#the humble manager
        # need to login, create shop and add items to it for test
        self.m.login_into_the_trading_system(self.u, "username", "password")
        self.m.login_into_the_trading_system(self.u2, "username2", "password2")
        self.m.login_into_the_trading_system(self.u3, "username3", "password3")
        self.m.shop_open(self.u, "shopname")
        self.m.shop_owner_assignment(self.u, "shopname", "username2")

    def tearDown(self):
        self.m.logout(self.u)
        self.m.logout(self.u2)

    def testGood(self):
        r = self.m.shop_manager_assignment(self.u, "shopname", "username3")
        ps = self.m.shop_manager_permissions_check(self.u,"shopname","username3")
        self.assertTrue((not ps.isexc), ps.exc)
        for i, bo in ps.res.items():
            if i == 12 or i== 13:
                self.assertTrue(bo,i)
            else:
                self.assertFalse(bo,i)

        self.m.shop_manager_permissions_delete(self.u2,"username3",12,"shopname")
        ps = self.m.shop_manager_permissions_check(self.u2, "shopname", "username3")
        self.assertTrue((not ps.isexc), ps.exc)
        for i, bo in ps.res.items():
            if i == 13:
                self.assertTrue(bo, i)
            else:
                pass#self.assertFalse(bo, i)
        self.m.shop_manager_permissions_add(self.u2,"username3",12,"shopname")
        ps = self.m.shop_manager_permissions_check(self.u2, "shopname", "username3")
        self.assertTrue((not ps.isexc), ps.exc)
        for i, bo in ps.res.items():
            if i == 12 or i == 13:
                self.assertTrue(bo, i)
            else:
                self.assertFalse(bo, i)


if __name__ == '__main__':
    unittest.main()
