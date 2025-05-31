from django.shortcuts import render

# Create your views here.


def view_returns(request):
    """ Renders content of returns page"""

    return render(request, 'returns/returns.html')
