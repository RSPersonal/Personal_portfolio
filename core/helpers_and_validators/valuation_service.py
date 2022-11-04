from website_projects.models import ScrapyPropertyModel
from core.helpers_and_validators.stock_calculator import calculate_mean_price
from typing import List, Type
from django.db.models import QuerySet


def get_properties_within_postal_code_range_and_nla_range(postal_code_range: List[str], user_input_type_object: str,
                                                          nla_range: int, user_input_city: str) -> Type[QuerySet]:
    """
    @param user_input_type_object:
    @param user_input_city:  str
    @param nla_range: int
    @param postal_code_range: list
    @return: list of queried properties
    """
    if not user_input_type_object:
        user_input_type_object = 'house'

    nla_lower_range = nla_range - (float(nla_range) * 0.10)
    nla_higher_range = nla_range + (float(nla_range) * 0.10)
    properties = ScrapyPropertyModel.objects.filter(type_of_property=user_input_type_object, city=user_input_city,
                                                    zipcode__range=(postal_code_range[0], postal_code_range[-1]),
                                                    woon_oppervlak__range=(nla_lower_range, nla_higher_range))
    return properties


def get_mean_property_price(properties: list):
    """
    @param properties: List of queried properties
    @return: Mean price of queried objects
    """
    if not properties:
        return 0

    price_list = []
    count_properties = 0
    for scraped_property in properties:
        count_properties += 1
        price_list.append(scraped_property.ask_price)
    mean_price = calculate_mean_price(price_list)
    return round(mean_price, 0)
