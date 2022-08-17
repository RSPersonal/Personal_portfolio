import unittest
from .extraction_helper import extract_postal_code


class TestExtractionHelper(unittest.TestCase):
    def test_extract_clean_postal_code(self):
        self.assertEqual(extract_postal_code('8021 DH'), '8021')


if __name__ == '__main__':
    unittest.main()
