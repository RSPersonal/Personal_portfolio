# from django.test import TestCase
# from . import models
#
# TEST_POSITION = 'Teststraat'
#
#
# def clean_up():
#     models.Positions.objects.get(po=TEST_POSITION).delete()
#
#
# class TestPositionModel(TestCase):
#     def setUp(self):
#         models.Positions.objects.create(street=TEST_STREETNAME)
#
#     def test_property_model_street(self):
#         test_instance = models.Positions.objects.get(street=TEST_STREETNAME)
#         self.assertEqual(test_instance.street, TEST_STREETNAME)
#         if test_instance:
#             clean_up()
