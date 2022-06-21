import unittest
import sys
#this is how you import from different folder in python:
#sys.path.insert(0, r'C:\Users\USER\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')

from Dev.ServiceLayer.SystemService import *

class MyTestCase(unittest.TestCase):


    def setUp(self):
        self.m=SystemService()
        self.m.initialization_of_the_system()
        
    def testGood(self):
        u=self.m.get_into_the_Trading_system_as_a_guest()
        r = self.m.is_active(u.res)
        self.assertTrue(not r.isexc and r.res,r.exc)
    def testDouble(self):
        u=self.m.get_into_the_Trading_system_as_a_guest()
        r = self.m.is_active(u.res)
        self.assertTrue(not r.isexc and r.res ,r.exc)
        u2=self.m.get_into_the_Trading_system_as_a_guest()
        r = self.m.is_active(u2.res)
        self.assertTrue(not r.isexc and r.res ,r.exc)
        r = self.m.is_active(u.res)
        self.assertTrue((not r.isexc) and r.res ,r.exc)
        self.assertFalse(u==u2)
        
if __name__ == '__main__':
    unittest.main()
