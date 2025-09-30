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
    
    if (!phone.startsWith('+')) {
        return false;
    }
    
    const cleanedPhone = phone.replace(/[^\d+]/g, '');
    
    // Check E.164 format: +[country code][number]
    // Country codes are 1-3 digits, total length should be 7-15 digits after +
    const e164Regex = /^\+[1-9]\d{6,14}$/;
    
    if (!e164Regex.test(cleanedPhone)) {
        return false;
    }
    
    const digits = cleanedPhone.substring(1); // Remove the +
    
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
    console.log('validateFormFields called');
    console.log('Form object:', form);
    
    if (!form) {
        console.error('Form not found!');
        return false;
    }
    
    // Check if form fields exist
    const formFields = ['customer_name', 'email', 'address', 'city', 'postcode', 'country', 'county', 'phone_number'];
    for (let fieldName of formFields) {
        if (!form[fieldName]) {
            console.error(`Field ${fieldName} not found in form!`);
        }
    }
    
    const requiredFields = [
        { field: document.getElementById('id_customer_name') || form.customer_name, name: 'Name' },
        { field: document.getElementById('id_email') || form.email, name: 'Email' },
        // Note: phone_number is optional at model level, validated separately
        { field: document.getElementById('id_address') || form.address, name: 'Address' },
        { field: document.getElementById('id_city') || form.city, name: 'City' },
        { field: document.getElementById('id_postcode') || form.postcode, name: 'Postal code' },
        { field: document.getElementById('id_country') || form.country, name: 'Country' },
        { field: document.getElementById('id_county') || form.county, name: 'County/State' }
    ];

    for (let item of requiredFields) {
        if (!item.field) {
            console.error(`Field not found: ${item.name}`);
            displayError(`Form field error: ${item.name} not found. Please refresh the page.`);
            return false;
        }
        
        const fieldValue = item.field.value ? item.field.value.trim() : '';
        console.log(`Checking ${item.name}: "${fieldValue}"`);
        
        // Extra validation for dropdown fields (like country)
        if (item.field.type === 'select-one' && (fieldValue === '' || fieldValue === 'Select Country *')) {
            console.log(`Validation failed for ${item.name}: dropdown not selected`);
            displayError(`Please select a ${item.name}.`);
            if (item.field.focus) item.field.focus(); 
            return false;
        }
        
        if (!fieldValue) {
            console.log(`Validation failed for ${item.name}: field is empty`);
            displayError(`Please fill in the ${item.name}.`);
            if (item.field.focus) item.field.focus(); 
            return false;
        }
        
        // Additional validation for specific fields
        if (item.field === (document.getElementById('id_address') || form.address) && fieldValue.length < 5) {
            console.log('Address validation failed: too short');
            displayError('Street address must be at least 5 characters long.');
            if (item.field.focus) item.field.focus();
            return false;
        }
        
        if (item.field === (document.getElementById('id_city') || form.city) && fieldValue.length < 2) {
            console.log('City validation failed: too short');
            displayError('City name must be at least 2 characters long.');
            if (item.field.focus) item.field.focus();
            return false;
        }
        
        if (item.field === (document.getElementById('id_county') || form.county) && fieldValue.length < 2) {
            console.log('County validation failed: too short');
            displayError('County/State must be at least 2 characters long.');
            if (item.field.focus) item.field.focus();
            return false;
        }
    }

    // 🔎 Extra validation: phone number format
    const phoneField = document.getElementById('id_phone_number') || form.phone_number;
    const phoneValue = phoneField ? phoneField.value.trim() : '';
    console.log(`Checking phone number: "${phoneValue}"`);
    if (phoneValue) {
        const isValid = isValidPhoneNumber(phoneValue);
        console.log(`Phone validation result: ${isValid}`);
        if (!isValid) {
            console.log('Phone validation failed');
            displayError("Please enter a valid phone number with country code (e.g., +12125551234, +44 7445 363737, +49 30 12345678) or leave the field empty.");
            if (phoneField && phoneField.focus) phoneField.focus();
            return false;
        }
    }

    console.log('All validation passed');
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
    
    console.log('Form submission prevented');
    console.log('Form element:', form);
    console.log('ErrorDiv element:', errorDiv);

    // Critical: Validate BEFORE any backend calls or payment processing  
    if (!validateFormFields()) {
        console.log('Validation failed - stopping submission');
        return;
    }
    
    console.log('Validation passed - proceeding with payment');

    try {
        
        if (!validateFormFields()) {
            return; 
        }
        
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

        // Double-check validation right before payment
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
            // Safety check before allowing form submission
            if (!validateFormFields()) {
                displayError('Validation error detected. Please contact support.');
                return;
            }
            
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
    const getFieldValue = (id, fallback) => {
        const element = document.getElementById(id) || (form && form[fallback]);
        return element ? element.value.trim() : '';
    };

    return {
        name: getFieldValue('id_customer_name', 'customer_name'),
        email: getFieldValue('id_email', 'email'),
        phone: getFieldValue('id_phone_number', 'phone_number'),
        address: {
            line1: getFieldValue('id_address', 'address'),
            city: getFieldValue('id_city', 'city'),
            postal_code: getFieldValue('id_postcode', 'postcode'),
            country: getFieldValue('id_country', 'country'),
            state: getFieldValue('id_county', 'county')
        },

    };
}

function getShippingDetails() {
    const getFieldValue = (id, fallback) => {
        const element = document.getElementById(id) || (form && form[fallback]);
        return element ? element.value.trim() : '';
    };

    return {
        name: getFieldValue('id_customer_name', 'customer_name'),
        phone: getFieldValue('id_phone_number', 'phone_number'),
        address: {
            line1: getFieldValue('id_address', 'address'),
            city: getFieldValue('id_city', 'city'),
            postal_code: getFieldValue('id_postcode', 'postcode'),
            country: getFieldValue('id_country', 'country'),
            state: getFieldValue('id_county', 'county')
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
    console.log('displayError called with:', message);
    
    if (!errorDiv) {
        console.error('errorDiv not found!');
        return;
    }
    
    const html = `
        <span class="invalid-icon" role="alert">
            <i class="fa-solid fa-square-xmark me-2"></i>
        </span>
        <span>${message}</span>
    `;
    errorDiv.innerHTML = html;
    
    // Make sure the error div is visible
    errorDiv.style.display = 'block';
    errorDiv.style.visibility = 'visible';
    
    console.log('Error displayed:', errorDiv.innerHTML);
    
    // Scroll to error message so user can see it
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
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