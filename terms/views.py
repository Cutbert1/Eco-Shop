from django.shortcuts import render

# Create your views here.


def view_terms(request):
    """ Renders content of terms page"""

    return render(request, 'terms/terms.html')
