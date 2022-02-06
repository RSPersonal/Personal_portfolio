from django.shortcuts import render


# Create your views here.
def home_page(request):
    """
    Function for homepage render
    """
    return render(request, 'home_page.html')


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
