from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models.functions import Lower
from django.db.models import Q

from .models import Product
from .forms import ProductForm


# Create your views here.


def fetch_all_products(request):
    """Fetch all products with optional search and category filtering."""
    products = Product.objects.all()
    search_query = request.GET.get('q', '').strip()
    categories = get_categories_from_request(request)
    sort = None
    direction = None
    current_sorting = 'None_None'

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        current_sorting = f'{sort}_{direction}'

    if categories:
        products = filter_products_by_category(products, categories)

    if search_query:
        if not search_query:
            messages.error(request, "There was no search criteria")
            return redirect(reverse('product'))
        products = filter_products_by_query(products, search_query)

    context = create_context(
        products, search_query, categories, current_sorting
        )
    return render(request, 'products/products.html', context)


def get_categories_from_request(request):
    """Extract categories from the request."""
    if 'category' in request.GET:
        return request.GET['category'].split(',')
    return None


def filter_products_by_category(products, categories):
    """Filter products based on selected categories."""
    return products.filter(category__name__in=categories)


def filter_products_by_query(products, query):
    """Filter products based on search query."""
    search_conditions = Q(name__icontains=query) | Q(
        description__icontains=query
    )
    return products.filter(search_conditions)


def create_context(products, search_term, categories, current_sorting):
    """Create context dictionary for rendering."""
    return {
        'products': products,
        'search_term': search_term,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }


def product_detail(request, product_id):
    """ Show specific product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add an item to product inventory """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been added successfully!')
            return redirect(reverse('add_product'))
        else:
            messages.error(
                request, 'Unable to add product. Please check the form.'  # noqa
                )
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
