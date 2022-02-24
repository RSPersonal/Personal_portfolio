from django.shortcuts import render


# Create your views here.
def home_page(request):
    """
    Function for homepage render
    """
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits' : num_visits
    }
    return render(request, 'home_page.html', context)


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
