from django import forms


class CurrencyForm(forms.Form):
    amount = forms.FloatField(label='amount')
