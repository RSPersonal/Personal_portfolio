import unittest


class TestStringMethods(unittest.TestCase):

    def test_split(self):
        test_string = 'test1, test2, test3'
        self.assertEqual(test_string.split(','), ['test1', ' test2', ' test3'])
        with self.assertRaises(TypeError):
            test_string.split(2)

    def test_strip_string(self):
        test_string = ' test1 '
        self.assertEqual(test_string.strip(), 'test1')


if __name__ == '__main__':
    unittest.main()
