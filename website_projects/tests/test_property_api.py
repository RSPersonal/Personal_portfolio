# import unittest
# import website_projects.models as models
#
# TEST_STREETNAME = 'Teststraat'
#
#
# def delete_test_entry():
#     if models.PropertyModel.objects.get(street='Teststraat'):
#         property_instance = models.PropertyModel.objects.get(street=TEST_STREETNAME)
#         property_instance.delete()
#
#
# def create_test_entry():
#     property_instance = models.PropertyModel(street=TEST_STREETNAME, housenumber='123')
#     property_instance.save()
#
#
# class TestPropertyModel(unittest.TestCase):
#
#     def test_property_model(self):
#         create_test_entry()
#         result = self.assertEqual(models.PropertyModel.objects.get(street=TEST_STREETNAME), TEST_STREETNAME)
#         if result:
#             delete_test_entry()
#
#
# if __name__ == '__main__':
#     unittest.main()
