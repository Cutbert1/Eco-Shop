// Core logic from stripe documentation //
var stripePublickey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublickey);
var elements = stripe.elements();

/* Core CSS from stripe documentation */
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#c40d20',
        iconColor: '#c40d20'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');



card.addEventListener('change', (event) => {
    const errorContainer = document.getElementById('card-errors');
 
    if (event.error) {
        errorContainer.innerHTML = createErrorMessage(event.error.message);
    } else {
        errorContainer.textContent = '';
    }
});
 
const createErrorMessage = (message) => `
    <span class="invalid-icon" role="alert">
        <i class="fa-solid fa-square-xmark me-2"></i>
    </span>
    <span class="small">${message}</span>
`;


// Form submit: Core logic from stripe documentation

const form = document.getElementById('payment-form');
const submitButton = document.getElementById('submit-button');
const errorDiv = document.getElementById('card-errors');
 
form.addEventListener('submit', async function(ev) {
    ev.preventDefault();
 
    try {
        disableForm();
 
        const billingDetails = getBillingDetails();
        const shippingDetails = getShippingDetails();
 
        
        var saveInfo = $('#id-save-info').prop('checked');
        
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
            'save_info': saveInfo,
        };
        var url = '/checkout/store_checkout_info/';
 
        
        await $.post(url, postData);
 
        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: { 
                card: card,
                billing_details: billingDetails
            },
            shipping: shippingDetails
        });
 
        if (result.error) {
            displayError(result.error.message);
        } else if (result.paymentIntent.status === 'succeeded') {
            form.submit();
        }
 
    } catch (error) {
        console.error('Payment processing error:', error);
        displayError('An unexpected error occurred. Please try again.');
    } finally {
        enableForm();
    }
});
 
function getBillingDetails() {
    
    return {
        name: form.customer_name.value.trim(),
        email: form.email.value.trim(),
        phone: form.phone_number.value.trim(),
        address: {
            line1: form.address.value.trim(),
            city: form.city.value.trim(),
            postal_code: form.postcode.value.trim(),
            country: form.country.value.trim(),
            state: form.county.value.trim()
        },
        
    };
}
 
function getShippingDetails() {
    
    return {
        name: form.customer_name.value.trim(),
        phone: form.phone_number.value.trim(),
        address: {
            line1: form.address.value.trim(),
            city: form.city.value.trim(),
            postal_code: form.postcode.value.trim(),
            country: form.country.value.trim(),
            state: form.county.value.trim()
        },
    };
    
}

function disableForm() {
    card.update({ disabled: true });
    submitButton.disabled = true;
}
 
function enableForm() {
    card.update({ disabled: false });
    submitButton.disabled = false;
}
 
function displayError(message) {
    const html = `
        <span class="invalid-icon" role="alert">
            <i class="fa-solid fa-square-xmark me-2"></i>
        </span>
        <span>${message}</span>
    `;
    errorDiv.innerHTML = html;
}