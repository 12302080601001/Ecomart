// scripts.js

// Function to update the cart count in the header
function updateCartCount() {
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    const cartCount = document.getElementById('cart-count');
    cartCount.textContent = cartItems.length;
}

// Function to handle adding to cart
function addToCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const product = getProductById(productId); // Assuming you have a function to get the product details
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

// Function to handle adding to wishlist
function addToWishlist(productId) {
    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    const product = getProductById(productId);
    wishlist.push(product);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
}

// Placeholder function to simulate fetching a product by ID (You would implement this function based on your data)
function getProductById(id) {
    const products = [
        { id: 1, name: 'Recycled Table', price: 50, description: 'A beautifully crafted recycled table', images: ['product1.png'] },
        { id: 2, name: 'Upcycled Chair', price: 30, description: 'A unique upcycled chair', images: ['product2.png'] },
        { id: 3, name: 'Recycled Shelf', price: 40, description: "A stylish recycled shelf", images: ['product3.png']},
        { id: 4, name: 'Upcycled Lamp', price: 20, description: "A charming upcycled lamp", images: ['product4.png']},
        
        // Add other products here...
    ];
    return products.find(product => product.id === id);
}

// Update cart count on page load
document.addEventListener('DOMContentLoaded', updateCartCount);
