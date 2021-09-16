from collections import namedtuple
from json.decoder import JSONDecodeError
from django.http.response import HttpResponse
from django.shortcuts import render
import requests
from django.http import JsonResponse

IP_ADDRESS = ''
JSON_ERROR = False

# Create your views here.
def index(request):
    if request.method == "POST":
        user_ip_input = request.POST.get('username')
        if user_ip_input != '':
            try:
                response=requests.get(f'http://api.ipstack.com/{user_ip_input}?access_key=9e190f3484c23275bc0cb044948ac119')
            except JSONDecodeError as e:
                print(e)
            
            geo_data = response.json()
            print(geo_data)
            if (geo_data['ip'] != ''):
                context = {
                    'ip' : geo_data['ip'],
                    'country_name' : geo_data['country_name']
                }
            else:
                return JsonResponse(geo_data)
    else:
        context = {
            'ip' : ''
        }
    return render(request, "api_examples.html", context)
