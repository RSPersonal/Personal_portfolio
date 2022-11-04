import requests
from website_projects.models import ScrapyPropertyModel
from datetime import datetime
from django.test import TestCase
from core.helpers_and_validators.valuation_service import get_mean_property_price, \
    get_properties_within_postal_code_range_and_nla_range


class TestValuationService(TestCase):
    def setUp(self) -> None:
        ScrapyPropertyModel.objects.create(
            street='Teststraat',
            housenumber=10,
            housenumber_add='A',
            zipcode='1234AZ',
            city='Teststad',
            municipality='Zwolle',
            type_of_property='Koophuis',
            ask_price=249000,
            amount_rooms=3,
            woon_oppervlak=120,
            perceel_oppervlak=200,
            status='Verkocht',
            date_sold=datetime.now()
        )
        ScrapyPropertyModel.objects.create(
            street='Teststraat',
            housenumber=20,
            housenumber_add='A',
            zipcode='1234AZ',
            city='Teststad',
            municipality='Zwolle',
            type_of_property='Koophuis',
            ask_price=460000,
            amount_rooms=3,
            woon_oppervlak=120,
            perceel_oppervlak=200,
            status='Verkocht',
            date_sold=datetime.now()
        )

    def test_get_single_scraped_property(self):
        fetched_property = ScrapyPropertyModel.objects.get(housenumber=10)
        self.assertEqual(fetched_property.housenumber, 10)
        self.assertEqual(fetched_property.housenumber_add, 'A')
        self.assertEqual(fetched_property.zipcode, '1234AZ')
        self.assertEqual(fetched_property.city, 'Teststad')
        self.assertEqual(fetched_property.municipality, 'Zwolle')
        self.assertEqual(fetched_property.type_of_property, 'Koophuis')
        self.assertEqual(fetched_property.ask_price, 249000)
        self.assertEqual(fetched_property.amount_rooms, 3)
        self.assertEqual(fetched_property.woon_oppervlak, 120)
        self.assertEqual(fetched_property.perceel_oppervlak, 200)
        self.assertEqual(fetched_property.status, 'Verkocht')

    def test_get_postal_code_range(self):
        postal_code_range = requests.get(
            'http://postcode.vanvulpen.nl/afstand/8021/3000/').json()
        self.assertEqual(postal_code_range, ['8011', '8012', '8019', '8021', '8022', '8023', '8031', '8032', '8033'])

    def test_get_properties_within_postal_code_range_and_nla_range(self):
        fetched_properties = get_properties_within_postal_code_range_and_nla_range(['1234AZ', '1234AZ'],
                                                                                   'Koophuis',
                                                                                   120,
                                                                                   'Teststad'
                                                                                   )
        self.assertTrue(fetched_properties)
        self.assertEqual(len(fetched_properties), 2)

    def test_get_mean_price(self):
        fetched_properties = get_properties_within_postal_code_range_and_nla_range(['1234AZ', '1234AZ'],
                                                                                   'Koophuis',
                                                                                   120,
                                                                                   'Teststad'
                                                                                   )
        mean_price = get_mean_property_price(fetched_properties)
        self.assertEqual(mean_price, 354500)
