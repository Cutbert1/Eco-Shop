from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q  # noqa

from .models import Product


# Create your views here.


def fetch_all_products(request):
    """Fetch all products with optional search functionality."""
    products = Product.objects.all()
    search_query = request.GET.get('q', None)

    if search_query:
        if not search_query.strip():
            messages.error(request, "There was no search parameter")
            return redirect(reverse('product'))

        products = filter_products_by_query(products, search_query)

    context = create_context(products, search_query)
    return render(request, 'products/products.html', context)


def filter_products_by_query(products, query):
    """Filter products based on the search query."""
    search_conditions = Q(name__icontains=query) | Q(
        description__icontains=query
        )
    return products.filter(search_conditions)


def create_context(products, search_term):
    """Create context dictionary for rendering."""
    return {
        'products': products,
        'search_term': search_term,
    }


def product_detail(request, product_id):
    """ Show specific product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)
