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

// Enhanced phone number validation function
function isValidPhoneNumber(phoneNumber) {
    if (!phoneNumber || phoneNumber.trim() === '') {
        return false;
    }
    
    const phone = phoneNumber.trim();
    
    // Must start with +
    if (!phone.startsWith('+')) {
        return false;
    }
    
    // Remove all formatting (spaces, dashes, parentheses) but keep the +
    const cleanedPhone = phone.replace(/[^\d+]/g, '');
    
    // Check E.164 format: +[country code][number]
    // Country codes are 1-3 digits, total length should be 7-15 digits after +
    const e164Regex = /^\+[1-9]\d{6,14}$/;
    
    if (!e164Regex.test(cleanedPhone)) {
        return false;
    }
    
    // Additional checks for common patterns
    const digits = cleanedPhone.substring(1); // Remove the +
    
    // Must have at least 7 digits (minimum for international numbers)
    if (digits.length < 7 || digits.length > 14) {
        return false;
    }
    
    // Country code validation (first 1-3 digits)
    const firstDigit = digits[0];
    
    // Common country code patterns
    if (firstDigit === '0') {
        return false; // No country codes start with 0
    }
    
    return true;
}

// Validate checkout form fields

function validateFormFields() {
    const requiredFields = [
        { field: form.customer_name, name: 'Name' },
        { field: form.email, name: 'Email' },
        // Note: phone_number is optional at model level, validated separately
        { field: form.address, name: 'Address' },
        { field: form.city, name: 'City' },
        { field: form.postcode, name: 'Postal code' },
        { field: form.country, name: 'Country' },
        { field: form.county, name: 'County/State' }
    ];

    for (let item of requiredFields) {
        if (!item.field.value.trim()) {
            displayError(`Please fill in the ${item.name}.`);
            return false;
        }
    }

    // 🔎 Extra validation: phone number format (optional but must be valid if provided)
    const phoneValue = form.phone_number.value.trim();
    if (phoneValue) {
        if (!isValidPhoneNumber(phoneValue)) {
            displayError("Please enter a valid phone number with country code (e.g., +12125551234, +44 7445 363737, +49 30 12345678) or leave the field empty.");
            return false;
        }
    }

    errorDiv.innerHTML = '';
    return true;
}

// Form submit: Core logic from stripe documentation

const form = document.getElementById('payment-form');
const submitButton = document.getElementById('submit-button');
const errorDiv = document.getElementById('card-errors');
const feedbackDiv = document.getElementById('payment-feedback');

form.addEventListener('submit', async function(ev) {
    ev.preventDefault();

    if (!validateFormFields()) {
        return;
    }

    try {
        disableForm();
        showFeedback('Authorising your payment. Please do not refresh...', 'info');

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

        // Final validation check before payment (double-check for Heroku)
        if (!validateFormFields()) {
            throw new Error('Form validation failed before payment');
        }

        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: billingDetails
            },
            shipping: shippingDetails
        });

        if (result.error) {
            displayError(result.error.message);
            showFeedback(result.error.message, 'error');
        } else if (result.paymentIntent.status === 'succeeded') {
            showFeedback('Payment confirmed! Redirecting to your receipt...', 'success');
            form.submit();
        }

    } catch (error) {
        console.error('Payment processing error:', error);
        displayError('An unexpected error occurred. Please try again.');
        showFeedback('Something went wrong while confirming your payment. Please review the errors above.', 'error');
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

function showFeedback(message, state = 'info') {
    if (!feedbackDiv) return;

    const stateClass = {
        success: 'alert alert-success',
        error: 'alert alert-danger',
        info: 'alert alert-info',
    }[state] || 'alert alert-info';

    feedbackDiv.className = `${stateClass}`;
    feedbackDiv.innerHTML = `
        <i class="fa-solid ${state === 'success' ? 'fa-circle-check' : state === 'error' ? 'fa-circle-exclamation' : 'fa-circle-info'} me-2"></i>${message}
    `;
}