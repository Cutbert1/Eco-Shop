from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models.functions import Lower
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import ProductForm


# Create your views here.


def fetch_all_products(request):
    """
    Fetch and display all products with optional sorting, searching,
    and category filtering.

    - Sorting by name or other fields with ascending/descending order.
    - Filtering by one or more categories.
    - Searching products by name or description.

    Renders:
        products/products.html with the filtered product list
        and context for sorting and filtering UI.
    """
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


@login_required(login_url='/accounts/login/')
def add_product(request):
    """
    Handles the addition of a new product to the inventory.

    - Only accessible by logged-in superusers;
      others are redirected with an error.
    - Handles form submission via POST to create a new product.
    - On successful creation, redirects to the product detail page.
    - On GET or invalid POST, renders the add product form.

    Template:
        products/add_product.html

    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Unable to add product. Only admin can add product'
            )
        return redirect(reverse('home'))

    def handle_post_request(request):

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Successfully added {product.name}')
            return redirect_to_product_detail(product.id)

        messages.error(
            request, 'Unable to add product. Please check the form.'
            )
        return render_add_product_form(form)

    def redirect_to_product_detail(product_id):

        return redirect(reverse('product_detail', args=[product_id]))

    def render_add_product_form(form=None):

        form = form or ProductForm()
        template = 'products/add_product.html'
        context = {'form': form}
        return render(request, template, context)

    if request.method == 'POST':
        return handle_post_request(request)

    return render_add_product_form()


@login_required(login_url='/accounts/login/')
def update_product(request, product_id):
    """
    Allow a superuser to update an existing product's details.

    Workflow:
    - Only accessible by logged-in superusers;
      others are redirected with an error.
    - Handles form submission via POST to update the product.
    - On GET, pre-fills the form with the current product data.
    - Shows success or error messages based on the outcome.

    Template:
        products/update_product.html
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Unable to update product. Only admin can update product'
            )
        return redirect(reverse('home'))

    def get_product(product_id):

        return get_object_or_404(Product, pk=product_id)

    def handle_post_request(request, product):

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

        form = ProductForm(instance=product)
        messages.info(request, f'You are updating {product.name}')
        return form

    product = get_product(product_id)

    if request.method == 'POST':
        form = handle_post_request(request, product)
        if isinstance(form, ProductForm):
            pass
        else:
            return form
    else:
        form = handle_get_request(product)

    template = 'products/update_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required(login_url='/accounts/login/')
def delete_product(request, product_id):
    """
    Allow a superuser to delete a product from the inventory.

    - Only accessible to logged-in superusers;
      others are redirected with an error.
    - Deletes the specified product by ID.
    - Shows a success message after deletion.
    - Redirects to the product list page.

    Args:
        request: HTTP request object.
        product_id: Primary key of the product to delete.
    """
    if not request.user.is_superuser:
        messages.error(
            request, 'Unable to delete product. Only admin can delete product'
            )
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(
        request, f'{product.name} has been removed from inventory!'
        )
    return redirect(reverse('products'))
