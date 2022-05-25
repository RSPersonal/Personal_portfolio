import unittest
from ..core_scripts import keyword_finder_core


class TestKeywordFinder(unittest.TestCase):
    def test_find_keyword(self):
        result = keyword_finder_core.find_keywords_in_text_file('valuation_', 'json', '../static/test_files/keyword_finder_test_file.txt')
        print(result)


if __name__ == '__main__':
    unittest.main()
