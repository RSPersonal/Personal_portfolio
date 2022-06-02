from django import forms
from .models import PropertyModel


class FilterForm(forms.ModelForm):
    # city = forms.ModelChoiceField(queryset=PropertyModel.objects.get(), empty_label=None)

    class Meta:
        model = PropertyModel
        fields = ['city', 'ask_price', 'building_type']
        widgets = {
            'city': forms.Select(),
        }
