import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.login_into_the_trading_system(self.u, "Alex", "Alex_123456")
        self.u2 = self.m.get_into_the_Trading_system_as_a_guest().res
        self.m.registration_for_the_trading_system(self.u2, "username", "password")

    def tearDown(self):
        self.m.logout(self.u)

    def testGood1(self):
        r = self.m.get_all_members_name(self.u)
        self.assertEqual(r.res[1][0], "username", , r.res)
        self.assertEqual(r.res[0][0], "Alex", , r.res)
        self.assertTrue((not r.isexc), r.exc)

    def testBad1(self):
        r = self.m.get_all_members_name(self.u2)
        self.assertTrue(r.isexc, r.exc)

    def testGood2(self):
        r = self.m.get_member_info(self.u, "Alex")
        self.assertTrue("Admin" in r.res, r.exc)
        self.assertTrue((not r.isexc), r.exc)

    def testBad2(self):
        r = self.m.get_member_info(self.u, "notMember")
        self.assertTrue(r.isexc, r.exc)


if __name__ == '__main__':
    unittest.main()
