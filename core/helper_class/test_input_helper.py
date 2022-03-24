import unittest
from input_validator_helper import *


class TestInputHelper(unittest.TestCase):

    def test_input_helper_value(self):
        self.assertEqual(value(''), False)


if __name__ == '__main__':
    unittest.main()
