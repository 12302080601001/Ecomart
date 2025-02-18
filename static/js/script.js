// Function to update the cart count in the header
function updateCartCount() {
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCount = document.getElementById('cart-count');
    cartCount.textContent = cartItems.length;
}

// Function to update the wishlist count in the header
function updateWishlistCount() {
    const wishlistItems = JSON.parse(localStorage.getItem('wishlist')) || [];
    const wishlistCount = document.getElementById('wishlist-count');
    if (wishlistCount) {
        wishlistCount.textContent = wishlistItems.length;
    }
}

// Function to fetch product details dynamically from the server
async function getProductById(id) {
    try {
        const response = await fetch(`/product_details/${id}`);
        if (!response.ok) throw new Error("Product not found");
        return await response.json(); // Assuming you return JSON from Flask
    } catch (error) {
        console.error("Error fetching product:", error);
        return null;
    }
}

// Function to handle adding to cart
async function addToCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const product = await getProductById(productId);
    
    if (product) {
        cart.push(product);
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
        alert(`${product.name} added to cart!`);
    } else {
        alert("Product not found!");
    }
}

// Function to handle adding to wishlist
async function addToWishlist(productId) {
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    const product = await getProductById(productId);
    
    if (product) {
        wishlist.push(product);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        updateWishlistCount();
        alert(`${product.name} added to wishlist!`);
    } else {
        alert("Product not found!");
    }
}

// Function to validate the payment form
function validatePaymentForm(event) {
    event.preventDefault();

    const addressSelect = document.getElementById("address-select");
    const newAddress = document.getElementById("new-address").value.trim();
    const cardNumber = document.getElementById("card-number").value.trim();
    const expiryDate = document.getElementById("expiry-date").value.trim();
    const cvv = document.getElementById("cvv").value.trim();

    // Check if an address is selected or entered
    if (!addressSelect.value && !newAddress) {
        alert("Please select or enter an address.");
        return;
    }

    // Validate card number (simple check for 16 digits)
    if (!/^\d{16}$/.test(cardNumber.replace(/\s/g, ""))) {
        alert("Invalid card number! Enter a 16-digit number.");
        return;
    }

    // Validate expiry date (MM/YY format)
    if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(expiryDate)) {
        alert("Invalid expiry date! Use MM/YY format.");
        return;
    }

    // Validate CVV (3 digits)
    if (!/^\d{3}$/.test(cvv)) {
        alert("Invalid CVV! Enter a 3-digit number.");
        return;
    }

    // Simulate payment processing
    simulatePayment();
}

// Fake payment processing function
function simulatePayment() {
    alert("Processing payment...");

    setTimeout(() => {
        const isSuccess = Math.random() > 0.2; // 80% chance of success
        if (isSuccess) {
            alert("Payment successful! Thank you for your purchase.");
            localStorage.removeItem("cart"); // Clear cart after successful payment
            window.location.href = "/"; // Redirect to home page
        } else {
            alert("Payment failed! Please try again.");
        }
    }, 2000); // Simulate a 2-second delay
}

// Function to handle submitting product reviews
async function submitReview(productId) {
    const reviewText = document.getElementById("review-text").value;
    const rating = document.getElementById("rating").value;

    if (!reviewText || !rating) {
        alert("Please provide a rating and review text.");
        return;
    }

    try {
        const response = await fetch(`/submit_review/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ reviewText, rating })
        });

        if (response.ok) {
            alert("Review submitted successfully!");
            location.reload(); // Reload to show updated reviews
        } else {
            alert("Failed to submit review. Please try again.");
        }
    } catch (error) {
        console.error("Error submitting review:", error);
        alert("Failed to submit review. Please try again.");
    }
}

// Function to display existing product reviews
async function fetchReviews(productId) {
    try {
        const response = await fetch(`/get_reviews/${productId}`);
        const reviews = await response.json();
        const reviewsContainer = document.getElementById("reviews-container");

        if (reviews.length === 0) {
            reviewsContainer.innerHTML = "<p>No reviews yet.</p>";
        } else {
            reviewsContainer.innerHTML = reviews.map(review => `
                <div class="review">
                    <div class="review-rating">Rating: ${review.rating} stars</div>
                    <div class="review-text">${review.reviewText}</div>
                </div>
            `).join("");
        }
    } catch (error) {
        console.error("Error fetching reviews:", error);
    }
}

// Initialize product reviews when the page loads
document.addEventListener("DOMContentLoaded", function () {
    updateCartCount();
    updateWishlistCount();

    // Get the product ID from the URL (assuming it's in the URL)
    const productId = window.location.pathname.split("/").pop();
    fetchReviews(productId);

    const reviewForm = document.getElementById("review-form");
    if (reviewForm) {
        reviewForm.addEventListener("submit", function(event) {
            event.preventDefault();
            submitReview(productId);
        });
    }
});
