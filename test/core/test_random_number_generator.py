import unittest
from core.helpers_and_validators.random_generator import generate_random_number


class TestRandomNumberGenerator(unittest.TestCase):

    def test_random_number_generator(self):
        self.assertIn(generate_random_number(0, 500), range(0, 500))


if __name__ == '__main__':
    unittest.main()
