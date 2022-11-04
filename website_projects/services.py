from .models import PropertyModel
from typing import Type, Union
from django.db.models import QuerySet


def get_all_active_cities(property_manager: Type[PropertyModel]) -> Union[QuerySet]:
    """
    @param property_manager: Instance of property model manager
    @return:QuerySet: All active property model cities
    """
    active_cities = property_manager.objects.all().values_list('city', flat=True).distinct()
    return active_cities
