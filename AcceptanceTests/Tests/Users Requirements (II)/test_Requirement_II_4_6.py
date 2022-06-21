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
        self.m.shop_owner_assignment(self.u, "shopname", "username3")
        self.passed = 0

    def tearDown(self):
        self.m.logout(self.u)
        self.m.logout(self.u2)

    def testGood(self):
        r = self.m.shop_manager_assignment(self.u, "shopname", "username2")
        if r.isexc:
            print(r.exc)
        self.assertTrue(r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)
        # r = self.m.shop_manager_permissions_check(self.u,"username2","shopname")
        # self.assertTrue(r.response, r.exc)
        self.assertTrue((not r.is_exception), r.exc)

    def testDouble(self):
        t1 = threading.Thread(target=self.assignusertoshop, args=[self.u, "username2", "shopname"])
        t2 = threading.Thread(target=self.assignusertoshop, args=[self.u3, "username2", "shopname"])
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print(self.m.shop_manager_permissions_check(self.u, "username2", "shopname").res)

    def assignusertoshop(self, tok, shopname, username):
        r1 = self.m.shop_manager_assignment(tok, shopname, username)
        self.assertTrue(r1.res, r.exc)
        self.assertTrue((not r1.isexc), r.exc)


if __name__ == '__main__':
    unittest.main()
