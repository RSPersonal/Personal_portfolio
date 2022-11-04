from django.test import TestCase
from django.test import Client
from .models import VisitorCount


class TestClient(TestCase):

    def setUp(self):
        """
        @return:
        """
        self.client = Client()

    def test_main_homepage_en(self):
        """
        @return:
        """
        homepage = self.client.get('/')
        self.assertEqual(homepage.status_code, 200)

    def test_contact_page(self):
        """
        @return:
        """
        homepage = self.client.get('/contact')
        self.assertEqual(homepage.status_code, 200)

    def test_api_example_page(self):
        """
        @return:
        """
        homepage = self.client.get('/api/v1/')
        self.assertEqual(homepage.status_code, 200)
