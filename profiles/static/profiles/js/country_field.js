// Get the country select element
const countrySelect = document.getElementById('id_primary_country');
 
// Function to set the color based on selection
function setColor(element) {
    if (!element.value) {
        element.style.color = '#aab7c4';
    } else {
        element.style.color = '#000';
    }
}
 
// Set initial color
setColor(countrySelect);
 
// Add event listener for changes
countrySelect.addEventListener('change', function() {
    setColor(this);
});