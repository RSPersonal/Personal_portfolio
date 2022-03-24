import unittest
import os
from decouple import config


class TestEnvKeys(unittest.TestCase):

    def test_db_keys_os_host(self):
        self.assertEqual(os.getenv('DB_HOST'), None)

    def test_db_keys_local_host(self):
        self.assertEqual(config('DB_HOST'), 'localhost')


if __name__ == '__main__':
    unittest.main()
