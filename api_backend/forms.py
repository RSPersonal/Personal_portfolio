from django import forms


class CurrencyForm(forms.Form):
    currency_symbol_to = forms.CharField(label='to-currency', max_length=20)
    amount = forms.IntegerField(label='amount')
