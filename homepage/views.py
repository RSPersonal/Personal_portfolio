from django.shortcuts import render, get_object_or_404
from .models import VisitorCount


# Create your views here.
def home_page(request):
    """
    Function for homepage render
    """
    num_visit = VisitorCount.objects.all()[1]
    num_visit.visitor_count += 1

    num_visit.save()

    num_current_visits = VisitorCount.objects.get(pk=1)
    # num_current_visits = 0

    context = {
        'num_visits': num_current_visits
    }
    return render(request, 'homepage.html', context)


def about_me(request):
    """
    Function for about me render
    """
    return render(request, 'about_me.html')


def contact(request):
    """
    Function for contact render
    """
    return render(request, 'contact.html')
