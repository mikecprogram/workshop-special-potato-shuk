import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):#remove member
        self.m = SystemService()
        self.m.initialization_of_the_system()
        self.u = self.m.get_into_the_Trading_system_as_a_guest().res
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
        self.m.login_into_the_trading_system(self.u, "Alex", "Alex_123456")

    def tearDown(self):
        self.m.logout(self.u)
        self.m.logout(self.u1)
        self.m.logout(self.u2)
        self.m.logout(self.u3)
        self.m.logout(self.u4)

    def testGood(self):
        r= self.m.shop_open(self.u1, "shopname")
        self.assertFalse(r.isexc, r.exc)
        r= self.m.shop_owner_assignment(self.u1, "shopname", "username2")
        self.assertFalse(r.isexc, r.exc)
        r= self.m.shop_manager_assignment(self.u1, "shopname", "username3")
        self.assertFalse(r.isexc, r.exc)
        # print(self.m.get_all_members_name(self.u).response)
        r= self.m.delete_member(self.u, 'username1')
        self.assertTrue( r.isexc,r.exc)
        r= self.m.delete_member(self.u, 'username2')
        self.assertTrue( r.isexc,r.exc)
        r= self.m.delete_member(self.u, 'username3')
        self.assertTrue( r.isexc,r.exc)
        r= self.m.delete_member(self.u, 'username4')
        self.assertFalse( r.isexc,r.exc)

    def testBad(self):
        # print(self.m.get_all_members_name(self.u).response)
        online_members = ['Alex', 'username1']
        r = True
        for i in online_members:
            r = r and self.m.delete_member(self.u, i).isexc
        # print(self.m.get_all_members_name(self.u).response)
        self.assertTrue(r, r.exc)


if __name__ == '__main__':
    unittest.main()
