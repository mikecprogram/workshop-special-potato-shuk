import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')

from SystemService import *

class MyTestCase(unittest.TestCase):


    def setUp(self):
        self.m=SystemService()
        
    def testGood(self):
        u=self.m.get_into_the_Trading_system_as_a_guest()
        r = self.m.is_active(u)
        self.assertTrue(not r.is_exception and r.response)
    def testDouble(self):
        u=self.m.get_into_the_Trading_system_as_a_guest()
        r = self.m.is_active(u)
        self.assertTrue(not r.is_exception and r.response)
        u2=self.m.get_into_the_Trading_system_as_a_guest()
        r = self.m.is_active(u2)
        self.assertTrue(not r.is_exception and r.response)
        r = self.m.is_active(u)
        self.assertTrue((not r.is_exception) and (not r.response))
        self.assertFalse(u==u2)
        
if __name__ == '__main__':
    unittest.main()
