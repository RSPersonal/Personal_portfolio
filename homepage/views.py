from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'home_page.html')

def about_me(request):
    return render(request, 'about_me.html')

def contact(request):
    return render(request, 'contact.html')