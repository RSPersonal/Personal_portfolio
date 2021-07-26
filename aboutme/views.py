"""Module to configure the app views"""
from django.shortcuts import render
from .models import LifeEvent

# Create your views here.
def about_me(request):
    """Return the about me template with life events db entries as a object"""
    live_events = LifeEvent.objects.all().order_by('created_on')
    context = {
        'live_events': live_events
    }
    return render(request, 'about_me.html', context)
