import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')
from SystemService import *


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.m=SystemService()
        self.u=self.m.get_into_the_Trading_system_as_a_guest().res
        
    def testGood(self):
        r = self.m.is_active(self.u)
        self.assertTrue((not r.isexc) and r.res)
        self.m.Trading_system_quitting(self.u)
        r = self.m.is_active(self.u)
        self.assertTrue((not r.isexc) and (not r.res))
        
if __name__ == '__main__':
    unittest.main()
