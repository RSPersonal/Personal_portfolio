import unittest
from core.helpers_and_validators.input_validator import value, no_value


class TestInputHelper(unittest.TestCase):

    def test_input_helper_value_empty(self):
        self.assertEqual(value(''), False)

    def test_input_helper_value(self):
        self.assertEqual(value('test'), True)

    def test_input_helper_no_value(self):
        self.assertEqual(no_value([]), True)


if __name__ == '__main__':
    unittest.main()
