from django.shortcuts import render
from .models import VisitorCount, ProfilePosts, VersionHistory
from homepage import services


# Create your views here.
def home_page_en(request):
    """
    Function for homepage render
    """
    active_visitor_count = services.check_if_active_visitor_count(VisitorCount)
    num_current_visits = 0
    if active_visitor_count:
        fetched_visitor_count_entry = services.get_database_entry_by_id(1, VisitorCount)
        fetched_visitor_count_entry.visitor_count += 1
        fetched_visitor_count_entry.save()

        num_current_visits = active_visitor_count

    profile_posts = ProfilePosts.objects.order_by('order').filter(language='EN')

    context = {
        'num_visits': num_current_visits,
        'profile_posts': profile_posts
    }
    return render(request, 'homepage_en.html', context)  # pragma no cover


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
    return render(request, 'homepage_nl.html', context)  # pragma no cover


def about_me(request):
    """
    Function for about me render
    """
    return render(request, 'about_me.html')  # pragma no cover


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
    return render(request, 'contact.html', context=context)  # pragma no cover
