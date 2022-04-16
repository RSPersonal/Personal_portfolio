import os
import unittest
import requests


class TestBackendApi(unittest.TestCase):
    def test_chart_api_connection(self):
        response = requests.request('GET', 'http://127.0.0.1:8000/api/v1/chart-data')
        response_json = response.json()
        self.assertEqual(response_json['message'], 'success')


if __name__ == '__main__':
    unittest.main()
