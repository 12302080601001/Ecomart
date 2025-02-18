from flask import Flask, render_template, request, redirect, url_for, session
import random
import string
import os
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key

# Image upload directory
UPLOAD_FOLDER = "static/uploads/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Predefined Users (In-memory database simulation)
users = {
    "buyer@example.com": {"password": generate_password_hash("buyerpassword"), "role": "buyer", "wishlist": [], "cart": []},
    "seller@example.com": {"password": generate_password_hash("sellerpassword"), "role": "seller", "wishlist": [], "cart": []}
}

# Mock Data for Products
products = [
    {"id": 1, "name": "Recycled Table", "price": 50, "description": "A beautifully crafted recycled table", "images": ["product1.png"]},
    {"id": 2, "name": "Upcycled Chair", "price": 30, "description": "A unique upcycled chair", "images": ["product2.png"]},
    {"id": 3, "name": "Recycled Shelf", "price": 40, "description": "A stylish recycled shelf", "images": ["product3.png"]},
    {"id": 4, "name": "Upcycled Lamp", "price": 20, "description": "A charming upcycled lamp", "images": ["product4.png"]},
    {"id": 5, "name": "Upcycled Denim Tote Bag", "price": 15, "description": "A trendy and durable tote bag made from old denim jeans.", "images": ["product5.png"]},
    {"id": 6, "name": "Recycled Paper Notebook", "price": 10, "description": "A sustainable notebook made from recycled paper.", "images": ["product6.png"]},
]

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    filtered_products = [p for p in products if search_query.lower() in p['name'].lower()] if search_query else products
    return render_template('index.html', products=filtered_products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and check_password_hash(users[email]['password'], password):
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

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email format."

        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            return "Password must contain at least 8 characters, including letters and numbers."

        if email in users:
            return "User already exists. Please log in."

        users[email] = {'password': generate_password_hash(password), 'role': role, 'wishlist': [], 'cart': []}
        session['user'] = email
        session['role'] = role
        return redirect(url_for('dashboard'))

    return render_template('signup.html')

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
    return render_template('product_details.html', product=product) if product else "Product not found."

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user' not in session or session.get('role') != 'seller':
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        image = request.files['image']

        if image:
            image_path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(image_path)

        new_product = {
            "id": len(products) + 1,
            "name": name,
            "price": price,
            "description": description,
            "images": [image.filename] if image else []
        }

        products.append(new_product)
        return redirect(url_for('dashboard'))

    return render_template('add_product.html')

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        users[session['user']]['cart'].append(product)
        return redirect(url_for('cart'))

    return "Product not found."

@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect(url_for('login'))

    cart = users[session['user']]['cart']
    return render_template('cart.html', cart=cart)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        address = request.form['address']
        card_number = request.form['card_number']
        expiry_date = request.form['expiry_date']
        cvv = request.form['cvv']

        # Simulate payment processing (random success or failure)
        if random.choice([True, False]):
            users[session['user']]['cart'].clear()  # Clear cart after successful purchase
            return redirect(url_for('order_success'))
        else:
            return redirect(url_for('order_failure'))

    return render_template('checkout.html')

@app.route('/order_success')
def order_success():
    return render_template('order_success.html')

@app.route('/order_failure')
def order_failure():
    return render_template('order_failure.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')

@app.route('/payment_failure')
def payment_failure():
    return render_template('payment_failure.html')

@app.route('/add_to_wishlist/<int:product_id>')
def add_to_wishlist(product_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        users[session['user']]['wishlist'].append(product)
        return redirect(url_for('wishlist'))

    return "Product not found."

@app.route('/wishlist')
def wishlist():
    if 'user' not in session:
        return redirect(url_for('login'))

    wishlist = users[session['user']]['wishlist']
    return render_template('wishlist.html', wishlist=wishlist)

if __name__ == '__main__':
    app.run(debug=True)
