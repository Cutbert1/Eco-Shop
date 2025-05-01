from django.shortcuts import render

# Create your views here.


def view_basket(request):
    """ Renders content of backet page"""

    return render(request, 'basket/basket.html')
