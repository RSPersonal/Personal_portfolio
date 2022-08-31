import unittest
from core.core_scripts.keyword_finder_core import find_keywords_in_text_file


class TestKeywordFinder(unittest.TestCase):
    def test_find_keyword(self):
        result = find_keywords_in_text_file('valuation_', 'json',
                                                                '../static/test_files/keyword_finder_test_file.txt')


if __name__ == '__main__':
    unittest.main()
