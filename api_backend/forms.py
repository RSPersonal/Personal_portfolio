from django import forms


class CurrencyForm(forms.Form):
    currency_symbol_to = forms.CharField(label='Currency', max_length=20)
