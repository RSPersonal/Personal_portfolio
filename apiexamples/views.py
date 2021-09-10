from django.shortcuts import render
import requests

DOMAIN_NAME = '2001:1c06:1e0c:1400:a13c:7679:d9ae:35ef'
# Create your views here.
def index(request):
    response=requests.get(f'http://api.ipstack.com/{DOMAIN_NAME}?access_key=9e190f3484c23275bc0cb044948ac119')
    geo_data= response.json()
    context= {
        'ip': geo_data['ip'],
        'country_name' : geo_data['country_name']
    }
    return render(request, 'api_examples.html', context)