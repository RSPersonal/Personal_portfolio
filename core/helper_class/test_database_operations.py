import os
import unittest
import psycopg2
from psycopg2 import Error
from decouple import config


class TestInsertRows(unittest.TestCase):

    def test_database_connection(self):
        try:
            conn = psycopg2.connect(dbname=os.getenv("DB_NAME", config("DB_NAME")),
                                    user=os.getenv("DB_USERNAME", config("DB_USERNAME")),
                                    password=os.getenv("DB_PASSWORD", config("DB_PASSWORD")),
                                    port=os.getenv("DB_PORT", config("DB_PORT"))
                                    )
            cursor = conn.cursor()
            db_parameters = conn.get_dsn_parameters()
            self.assertEqual(db_parameters['user'], os.getenv("DB_USERNAME", config("DB_USERNAME")))
            conn.close()
        except (Exception, Error) as error:
            print("Error while connecting to PostgresSql", error)
        finally:
            if conn:
                cursor.close()
                conn.close()
                print("Postgresql connection is closed")

    def test_

if __name__ == '__main__':
    unittest.main()
