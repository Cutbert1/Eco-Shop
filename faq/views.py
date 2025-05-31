from django.shortcuts import render

# Create your views here.


def view_faq(request):
    """ Renders content of FAQ page"""

    return render(request, 'faq/faq.html')
