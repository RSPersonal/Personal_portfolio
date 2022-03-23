from django import forms


class PortfolioForm(forms.Form):
    portfolio_name = forms.CharField(label='Portfolio name', max_length=50)


class PositionForm(forms.Form):
    ticker_name = forms.CharField(max_length=40)
    buy_price = forms.FloatField()
    market = forms.CharField(max_length=20)
    quantity = forms.FloatField()
