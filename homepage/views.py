from django.shortcuts import render, redirect
from .models import VisitorCount, ProfilePosts


# Create your views here.
def home_page_en(request):
    """
    Function for homepage render
    """
    active_visitor_count = VisitorCount.objects.get(pk=1)
    if active_visitor_count:
        active_visitor_count.visitor_count += 1
        active_visitor_count.save()

    num_current_visits = active_visitor_count

    profile_posts = ProfilePosts.objects.order_by('order').filter(language='EN')

    context = {
        'num_visits': num_current_visits,
        'profile_posts': profile_posts
    }
    return render(request, 'homepage_en.html', context)


def home_page_nl(request):
    """
    Function for homepage render
    """
    active_visitor_count = VisitorCount.objects.get(pk=1)
    if active_visitor_count:
        active_visitor_count.visitor_count += 1
        active_visitor_count.save()

    num_current_visits = active_visitor_count

    profile_posts = ProfilePosts.objects.order_by('order').filter(language='NL')

    context = {
        'num_visits': num_current_visits,
        'profile_posts': profile_posts
    }
    return render(request, 'homepage_nl.html', context)


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
