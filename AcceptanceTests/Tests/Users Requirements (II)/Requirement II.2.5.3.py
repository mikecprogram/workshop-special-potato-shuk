import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def happyCase(self):
        pass

    def sadCase(self):
        pass

    def badCase(self):
        pass


if __name__ == '__main__':
    unittest.main()
