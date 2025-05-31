from django.shortcuts import render

# Create your views here.


def view_privacy(request):
    """ Renders content of privacy page"""

    return render(request, 'privacy/privacy.html')
