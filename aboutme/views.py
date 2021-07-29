"""Module to configure the app views"""
from django.shortcuts import render
from aboutme.models import LifeEvent

# Create your views here.
def about_me(request):
    """Return the about me template with life events db entries as a object"""
    events = LifeEvent.objects.all()
    context = {
        'events': events
    }
    return render(request, 'about_me.html', context)
