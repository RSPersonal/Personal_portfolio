from json.decoder import JSONDecodeError
from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def index(request):
    context = {}
    
    if request.method == "POST":
        user_ip_input = request.POST.get('ip-address')
        if user_ip_input != '':
            try:
                response=requests.get(f'http://api.ipstack.com/{user_ip_input}?access_key=9e190f3484c23275bc0cb044948ac119')
            except JSONDecodeError as e:
                print(e)
            
            geo_data = response.json()
            print(geo_data)
            if ('ip' in geo_data):
                context = {
                    'ip' : geo_data['ip'],
                    'country_name' : geo_data['country_name'],
                    'region_name' : geo_data['region_name'],
                    'city': geo_data['city'],
                    'latitude' : geo_data['latitude'],
                    'longitude' : geo_data['longitude']
                }
            else:
                return JsonResponse(geo_data)
        else:
            messages.add_message(request, messages.INFO, "Input field is empty, please enter you ip!")
    else:
        context = {}
    return render(request, "api_examples.html", context)
