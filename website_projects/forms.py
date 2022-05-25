from django.forms import ModelForm
from .models import PropertyModel


class FilterForm(ModelForm):
    class Meta:
        model = PropertyModel
        fields = ['city', 'ask_price']
