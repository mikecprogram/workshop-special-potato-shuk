#import unittest

class MarketTests(unittest.TestCase):
    def logintests(self):
        m = Market(None,None,None,None)
        self.testTimeout_guest(m)

    def testTimeout_guest(self):
        self.assertTrue(True, False)
if __name__ == '__main__':
    #unittest.main()
    mt = MarketTests()
    mt.logintests
