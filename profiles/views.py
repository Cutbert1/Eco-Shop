from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import AccountProfile
from .forms import AccountProfileForm
from checkout.models import Order

# Create your views here.


def profile(request):
    """ Show user profile. """
    def get_profile():
        """Get the user's profile or return 404 if not found."""
        return get_object_or_404(AccountProfile, user=request.user)

    def handle_post_request(profile):
        """Handle POST request for updating the profile."""
        form = AccountProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated Profile')
        return form

    def get_orders(profile):
        """Get all orders associated with the profile."""
        return profile.orders.all()

    def prepare_context(form, orders):
        """Prepare the context dictionary for rendering."""
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
