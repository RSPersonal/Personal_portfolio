from django.test import TestCase
from django.test import Client
from homepage.models import VisitorCount
from homepage.services import get_database_entry_by_id


class TestClient(TestCase):
    def setUp(self):
        """
        @return: Test client instance
        """
        self.client = Client()
        VisitorCount.objects.create(
            pk=1,
            visitor_count=1
        )

    def test_main_homepage_en(self) -> None:
        """
        @return: None
        """
        homepage = self.client.get('/')
        self.assertEqual(homepage.status_code, 200)

    def test_contact_page(self) -> None:
        """
        @return: None
        """
        contage_page = self.client.get('/contact')
        self.assertEqual(contage_page.status_code, 200)

    def test_api_example_page(self) -> None:
        """
        @return:None
        """
        api_example_page = self.client.get('/api/v1/')
        self.assertEqual(api_example_page.status_code, 200)

    def test_database_projects_page(self) -> None:
        """
        @return:None
        """
        database_projects_page = self.client.get('/database-projects')
        self.assertEqual(database_projects_page.status_code, 200)

    def test_website_projects_page(self) -> None:
        """
        @return:None
        """
        website_projects_page = self.client.get('/website-projects/')
        self.assertEqual(website_projects_page.status_code, 200)

    def test_get_database_entry_by_id(self):
        fetched_visitor_count_entry = get_database_entry_by_id(1, VisitorCount)
        self.assertEqual(fetched_visitor_count_entry.visitor_count, 1)
