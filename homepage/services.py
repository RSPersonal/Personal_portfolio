from typing import Union, Type
from django.db.models import QuerySet

from .models import VisitorCount


def check_if_active_visitor_count(model_instance: Type[VisitorCount]) -> bool:
    return model_instance.objects.filter(pk=1).exists()


def get_database_entry_by_id(requested_id: int, database_model: Type[VisitorCount]) -> Type[VisitorCount]:
    return database_model.objects.get(pk=requested_id)
