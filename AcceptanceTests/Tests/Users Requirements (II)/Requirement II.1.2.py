import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\SHUK1')

from market import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=marketService()
        self.u=self.m.enter()
        
    def testGood(self):
        self.assertTrue(self.m.isActive(u))
        self.m.exit(u)
        self.assertFalse(self.m.isActive(u))
        
if __name__ == '__main__':
    unittest.main()
