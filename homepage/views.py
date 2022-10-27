from django.shortcuts import render
from .models import VisitorCount, ProfilePosts, VersionHistory


# Create your views here.
def home_page_en(request):
    """
    Function for homepage render
    """
    check_active_visitor_count = VisitorCount.objects.filter(pk=1).exists()

    if check_active_visitor_count:
        active_visitor_count = VisitorCount.objects.get(pk=1)
        active_visitor_count.visitor_count += 1
        active_visitor_count.save()
        num_current_visits = active_visitor_count
    else:
        first_visitor_count = VisitorCount(visitor_count=1)
        first_visitor_count.save()
        num_current_visits = 1

    profile_posts = ProfilePosts.objects.order_by('order').filter(language='EN')

    # TODO Possible this can be done more elegant. Probably to many database calls
    if VersionHistory.objects.filter(pk=1).exists():
        with open('version.txt', 'r') as file:
            current_version_number = file.read()
            file.close()
        version_db_object = VersionHistory.objects.get(id=1)
        if version_db_object.version_number is not current_version_number:
            version_db_object.version_number = current_version_number
            version_db_object.save()
    else:
        # Get current version number from text file
        with open('version.txt', 'r') as file:
            current_version_from_txt = file.read()
            new_version_entry = VersionHistory(id=1, version_number=current_version_from_txt)
            new_version_entry.save()

    context = {
        'num_visits': num_current_visits,
        'profile_posts': profile_posts
    }
    return render(request, 'homepage_en.html', context)


def home_page_nl(request):
    """
    Function for homepage render
    """
    check_active_visitor_count = VisitorCount.objects.filter(pk=1).exists()

    if check_active_visitor_count:
        active_visitor_count = VisitorCount.objects.get(pk=1)
        active_visitor_count.visitor_count += 1
        active_visitor_count.save()
        num_current_visits = active_visitor_count
    else:
        first_visitor_count = VisitorCount(visitor_count=1)
        first_visitor_count.save()
        num_current_visits = 1

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
