from django.test import TestCase
from . import models

TEST_STREETNAME = 'Teststraat'


def clean_up():
    models.PropertyModel.objects.get(street=TEST_STREETNAME).delete()


class TestPropertyModel(TestCase):
    def setUp(self):
        models.PropertyModel.objects.create(street=TEST_STREETNAME)

    def test_property_model_street(self):
        test_instance = models.PropertyModel.objects.get(street=TEST_STREETNAME)
        self.assertEqual(test_instance.street, TEST_STREETNAME)
        if test_instance:
            clean_up()
