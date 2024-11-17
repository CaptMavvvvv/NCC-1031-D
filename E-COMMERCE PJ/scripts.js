// Initialize the cart as an empty array
let cart = [];

// Function to add products to the cart
function addToCart(id, name, price) {
    // Check if the product already exists in the cart
    const productInCart = cart.find(item => item.id === id);

    if (productInCart) {
        // If product exists, increase quantity
        productInCart.quantity += 1;
    } else {
        // If the product does not exist, add it to the cart
        cart.push({ id, name, price, quantity: 1 });
    }

    // Update the cart count and total price
    updateCartCount();
}

// Function to update the cart count in the top-right corner
function updateCartCount() {
    const cartCount = cart.reduce((total, item) => total + item.quantity, 0);
    document.getElementById('cart-count').innerText = cartCount;
}

// Function to calculate and display the total price (optional if needed in the main menu)
function calculateTotalPrice() {
    const totalPrice = cart.reduce((total, item) => total + item.price * item.quantity, 0);
    return totalPrice.toFixed(2);
}

// Optional: Display total price in the cart or main menu
function displayTotalPrice() {
    // This can be displayed wherever needed; for now, we log it
    console.log(`Total Price: $${calculateTotalPrice()}`);
}

document.getElementById('payment-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Collect the form data
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    const paymentMethod = document.getElementById('payment-method').value;
    const cardNumber = document.getElementById('card-number').value;
    const securityCode = document.getElementById('security-code').value;
    const expirationDate = document.getElementById('expiration-date').value;
    const cardholderName = document.getElementById('cardholder-name').value;

    // Basic validation (you can expand this as needed)
    if (cardNumber.length !== 16 || securityCode.length !== 3) {
        alert('Please enter valid card information.');
        return;
    }

    // Here you can add code to handle payment processing

    // Display a message to confirm submission (or redirect to a thank you page)
    alert(`Payment completed for ${name} using ${paymentMethod}`);
});
