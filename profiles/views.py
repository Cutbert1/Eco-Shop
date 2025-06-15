from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import AccountProfile
from .forms import AccountProfileForm
from checkout.models import Order

# Create your views here.


def profile(request):
    """
    Display and handle updates to the authenticated user's profile.

    GET:
        - Display user's profile details in a form.
        - Display list of user's orders.

    POST:
        - Process submitted profile update form.
        - If valid, save changes and display a success message.
        - If invalid, display an error message.
    """
    def get_profile():

        return get_object_or_404(AccountProfile, user=request.user)

    def handle_post_request(profile):
        form = AccountProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated Profile')
        else:
            messages.error(
                request, 'Update is unsuccessful. Please ensure form validity.'
                )

        return form

    def get_orders(profile):
        return profile.orders.all()

    def prepare_context(form, orders):
        return {
            'form': form,
            'orders': orders,
            'profile_page': True
        }

    profile = get_profile()

    if request.method == 'POST':
        form = handle_post_request(profile)
    else:
        form = AccountProfileForm(instance=profile)

    orders = get_orders(profile)
    context = prepare_context(form, orders)
    template = 'profiles/profile.html'

    return render(request, template, context)


def order_record(request, order_number):
    """
    Show a specific order's record for the user.

    Retrieves the order matching the order number,
    shows an information about the previous confirmation,
    and renders the order details using the checkout confirmation template.

    Args:
        request: HTTP request object.
        order_number (str): Unique identifier for the order.

    Returns:
        HttpResponse: Rendered page showing the order details.
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'Previous confirmation for order number {order_number}. '
        'Confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_complete.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
