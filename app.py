from flask import Flask, render_template, request, redirect, url_for, session
import random
import string
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a secure secret key

# Predefined Users (In-memory database simulation)
users = {
    "buyer@example.com": {"password": "buyerpassword", "role": "buyer", "wishlist": [], "cart": []},
    "seller@example.com": {"password": "sellerpassword", "role": "seller", "wishlist": [], "cart": []}
}

# Mock Data for Products
products = [
    {"id": 1, "name": "Recycled Table", "price": 50, "description": "A beautifully crafted recycled table", "images": ["product1.png"]},
    {"id": 2, "name": "Upcycled Chair", "price": 30, "description": "A unique upcycled chair", "images": ["product2.png"]},
    {"id": 3, "name": "Recycled Shelf", "price": 40, "description": "A stylish recycled shelf", "images": ["product3.png"]},
    {"id": 4, "name": "Upcycled Lamp", "price": 20, "description": "A charming upcycled lamp", "images": ["product4.png"]},
    # Add more products as needed...
]

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    if search_query:
        filtered_products = [product for product in products if search_query.lower() in product['name'].lower()]
    else:
        filtered_products = products

    return render_template('index.html', products=filtered_products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email]['password'] == password:
            session['user'] = email
            session['role'] = users[email]['role']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Please try again."
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Email format validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email format. Please enter a valid email."

        # Password strength check (at least 8 characters, including a number and a letter)
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            return "Password must be at least 8 characters long and contain both letters and numbers."

        if email in users:
            return "User already exists. Please log in."

        # Add the new user to the dictionary
        users[email] = {'password': password, 'role': role, 'wishlist': [], 'cart': []}
        session['user'] = email
        session['role'] = role
        return redirect(url_for('dashboard'))
    
    return render_template('signup.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        if email not in users:
            return "Email not found."

        # Generate a new password (for simplicity, using a random string)
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        users[email]['password'] = new_password
        return f"Your new password is: {new_password}"

    return render_template('forgot_password.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login')) 

    if session['role'] == 'seller':
        return render_template('seller_dashboard.html', products=products)
    else:
        return render_template('buyer_dashboard.html', products=products)

@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_details.html', product=product)
    return "Product not found."

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(product)
        return redirect(url_for('cart'))

    return "Product not found."

@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect(url_for('login'))

    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/checkout')
def checkout():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Simulating a successful payment (No real payment gateway)
    return render_template('checkout.html')

@app.route('/add_to_wishlist/<int:product_id>')
def add_to_wishlist(product_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        if 'wishlist' not in session:
            session['wishlist'] = []
        session['wishlist'].append(product)
        return redirect(url_for('wishlist'))

    return "Product not found."

@app.route('/wishlist')
def wishlist():
    if 'user' not in session:
        return redirect(url_for('login'))

    wishlist = session.get('wishlist', [])
    return render_template('wishlist.html', wishlist=wishlist)

if __name__ == '__main__':
    app.run(debug=True)
