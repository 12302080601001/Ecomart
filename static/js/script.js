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

// Update cart and wishlist count on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    updateWishlistCount();
});
