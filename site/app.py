from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import sqlite3
import json 

app = Flask(__name__, static_folder='static')


# Load configuration from config.json
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'config.json')

print(f"Attempting to load configuration from: {CONFIG_FILE_PATH}")

try:
    with open(CONFIG_FILE_PATH, 'r') as config_file:
        config_data = json.load(config_file)
        print(f"Successfully loaded configuration: {config_data}")
except Exception as e:
    print(f"Error loading configuration: {e}")
    config_data = {"website_title": "Default Title", "website_name": "Default Name"}

# Database path
db_path = 'data/product_links.db'

# Check if the database exists and create tables if necessary
def initialize_database():
    # Ensure the directory for the database file exists
    db_directory = os.path.dirname(db_path)
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the 'product_links' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS product_links (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      url TEXT)''')

    conn.commit()
    conn.close()


# Initialize the database
initialize_database()

@app.route('/')
def home():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM product_links')
    product_links = cursor.fetchall()

    conn.close()

    # Sort product links by the second element (product name) in ascending order
    sorted_product_links = sorted(product_links, key=lambda x: x[1])

    return render_template('index.html', product_links=sorted_product_links, website_title=config_data['website_title'], website_name=config_data['website_name'])

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    try:
        if request.method == 'POST':
            new_name = request.form.get('name')
            new_url = request.form.get('url')

            print(f"Received POST request with name: {new_name}, url: {new_url}")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute('INSERT INTO product_links (name, url) VALUES (?, ?)',
                           (new_name, new_url))

            conn.commit()
            conn.close()

            print("Product added successfully.")

            return redirect(url_for('home'))

        # If the request method is GET, render the form for adding a new product
        return render_template('add_product.html', website_title=config_data['website_title'], website_name=config_data['website_name'])

    except Exception as e:
        print("Error adding product to database:", str(e))
        return render_template('error.html', error_message="Error adding product to database.")

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_url = request.form.get('url')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('UPDATE product_links SET name=?, url=? WHERE id=?',
                       (new_name, new_url, id))

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product_links WHERE id=?', (id,))
    product = cursor.fetchone()
    conn.close()

    return render_template('edit.html', product=product, website_title=config_data['website_title'], website_name=config_data['website_name'])
    
@app.route('/delete_product/<int:id>')
def delete_product(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM product_links WHERE id=?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
