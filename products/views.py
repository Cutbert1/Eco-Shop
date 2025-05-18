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


def update_product(request, product_id):
    """ Update product details """
    def get_product(product_id):
        """ Get product object or return 404 """
        return get_object_or_404(Product, pk=product_id)

    def handle_post_request(request, product):
        """ Handle POST request for updating product """
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated {product.name}')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Update is unsuccessful. Please ensure form validity.'
            )
        return form

    def handle_get_request(product):
        """ Handle GET request for updating product """
        form = ProductForm(instance=product)
        messages.info(request, f'You are updating {product.name}')
        return form

    product = get_product(product_id)

    if request.method == 'POST':
        form = handle_post_request(request, product)
        if isinstance(form, ProductForm):
            # If form is returned, it means update was unsuccessful
            pass
        else:
            # If redirect is returned, it means update was successful
            return form
    else:
        form = handle_get_request(product)

    template = 'products/update_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)
