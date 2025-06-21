from django.shortcuts import render

# Create your views here.

def privacy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')

def contact(request):
    return render(request, 'core/contact.html')

def help_center(request):
    return render(request, 'core/help.html')
