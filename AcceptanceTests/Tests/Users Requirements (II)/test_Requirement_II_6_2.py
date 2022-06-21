import unittest
from Dev.ServiceLayer.SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
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

        self.m.shop_open(self.u1, "shopname")

    def tearDown(self):
        self.m.logout(self.u)
        self.m.logout(self.u1)
        self.m.logout(self.u2)
        self.m.logout(self.u3)
        self.m.logout(self.u4)

    def testGood(self):
        #print(self.m.get_all_members_name(self.u).response)
        online_members=['username2', 'username3', 'username4']
        r = False
        for i in online_members:
            r = r or self.m.delete_member(self.u,i).isexc
        #print(self.m.get_all_members_name(self.u).response)
        self.assertTrue(not r,r.exc)

    def testBad(self):
        #print(self.m.get_all_members_name(self.u).response)
        online_members = ['Alex', 'username1']
        r = True
        for i in online_members:
            r = r and self.m.delete_member(self.u, i).isexc
        #print(self.m.get_all_members_name(self.u).response)
        self.assertTrue(r,r.exc)


if __name__ == '__main__':
    unittest.main()
