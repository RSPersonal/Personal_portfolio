from website_projects.models import ScrapyPropertyModel
from core.helpers_and_validators.calculator import calculate_mean_price

def get_properties_within_postal_code_range_and_nla_range(postal_code_range: list, nla_range: list):
    """
    @param postal_code_range:
    @return:
    """
    properties = ScrapyPropertyModel.objects.filter(zipcode__range=(postal_code_range[0], postal_code_range[-1]))
    return properties


def get_mean_property_price(properties: list):
    """
    @param properties:
    @return:
    """
    if not properties:
        return 'Missing input properties'

    price_list = []
    count_properties = 0
    for scraped_property in properties:
        count_properties += 1
        price_list.append(scraped_property.ask_price)
    mean_price = calculate_mean_price(price_list)
    return mean_price
