import unittest
import requests


class TestValuationService(unittest.TestCase):
    #
    # def test_get_user_input_properties(self):
    #     nla_lower_range = 90 - (90 * 0.10)
    #     nla_higher_range = 90 + (90 * 0.10)
    #     self.assertEqual()

    def test_get_postal_code_range(self):
        postal_code_range = requests.get(
            'http://postcode.vanvulpen.nl/afstand/8021/3000/').json()
        self.assertEqual(postal_code_range, ['8011', '8012', '8019', '8021', '8022', '8023', '8031', '8032', '8033'])
