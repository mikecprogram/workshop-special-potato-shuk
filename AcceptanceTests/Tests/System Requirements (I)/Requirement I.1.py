import unittest
import sys
#this is how you import from different folder in python:
sys.path.insert(0, r'C:\Users\user\Desktop\workshop-special-potato-shuk\dev\ServiceLayer')

from SystemService import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.m=SystemService()
        
    def testGood(self):
        r = self.m.initialization_of_the_system()
        self.assertTrue((not r.isexc) and r.res ,r.exc)




    def happyCase(self):
        pass

    def sadCase(self):
        pass

    def badCase(self):
        pass


if __name__ == '__main__':
    unittest.main()
