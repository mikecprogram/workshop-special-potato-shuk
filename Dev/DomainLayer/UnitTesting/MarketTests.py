#import unittest
import unittest

from Dev.DomainLayer.Objects.Market import Market


class MarketTests(unittest.TestCase):
    def logintests(self):
        m = Market(None)
        self.testTimeout_guest(m)

    def testTimeout_guest(self):
        self.assertTrue(True, False)
if __name__ == '__main__':
    #unittest.main()
    mt = MarketTests()
    mt.logintests
