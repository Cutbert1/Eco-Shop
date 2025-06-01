from django.shortcuts import render

# Create your views here.


def view_blog(request):
    """ Renders content of blog page"""

    return render(request, 'blog/blog.html')
