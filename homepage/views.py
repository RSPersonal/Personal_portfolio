from django.shortcuts import render, redirect
from .models import VisitorCount, ProfilePosts, VersionHistory


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
    if VersionHistory.objects.filter(id=1).exists():
        current_version_number = VersionHistory.objects.get(id=1)
    else:
        # Get current version number from text file
        with open('version.txt', 'r') as file:
            current_version_from_txt = file.read()
            new_version_entry = VersionHistory(id=1, version_number=current_version_from_txt)
            new_version_entry.save()
            current_version_number = current_version_from_txt
    context = {'version_history': current_version_number}
    return render(request, 'contact.html', context=context)
