from typing import Type
from django.db.models import Model


def check_if_active_visitor_count(model_instance: Type[Model]) -> bool:
    return model_instance.objects.filter(pk=1).exists()


def get_database_entry_by_id(requested_id: int, database_model: Type[Model]) -> Type[Model]:
    return database_model.objects.get(pk=requested_id)
