from json.decoder import JSONDecodeError
from django.shortcuts import render
import requests

IP_ADDRESS = ''
JSON_ERROR = False

# Create your views here.
def index(request):
    if (request.GET.get('mybtn')):
        IP_ADDRESS = request.GET.get('mytextbox')
        
        try:
            response=requests.get(f'http://api.ipstack.com/{IP_ADDRESS}?access_key=9e190f3484c23275bc0cb044948ac119')
        except JSONDecodeError as e:
            JSON_ERROR == True
                
        try:
            geo_data= response.json()
        except JSONDecodeError as e:
            JSON_ERROR == True

        
        if (JSON_ERROR != False):
            context= {
            'ip': geo_data['ip'],
            'country_name' : geo_data['country_name']
            }
        else:
            context = {
                'ip': 'No IP address entered',
                'country_name': 'No country found, check error message'
            }
        
    return render(request, 'api_examples.html', context)