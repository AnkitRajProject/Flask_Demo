from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('customers.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get customer names for the dropdown
@app.route('/get_customers')
def get_customers():
    conn = get_db_connection()
    customers = conn.execute('SELECT customer_id, first_name, last_name FROM Customers').fetchall()
    conn.close()
    return jsonify([dict(row) for row in customers])

# Route to get details of a selected customer including orders and shipping info
@app.route('/get_customer_details/<int:id>')
def get_customer_details(id):
    conn = get_db_connection()
    
    # Fetch customer details
    customer = conn.execute('SELECT * FROM Customers WHERE customer_id = ?', (id,)).fetchone()
    if customer is None:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404
    
    # Fetch orders for the customer
    orders = conn.execute('SELECT * FROM Orders WHERE customer_id = ?', (id,)).fetchall()
    
    # Fetch shipping info for the customer
    shippings = conn.execute('SELECT * FROM Shippings WHERE customer = ?', (id,)).fetchall()
    
    conn.close()
    
    customer_details = dict(customer)
    customer_details['orders'] = [dict(order) for order in orders]
    customer_details['shippings'] = [dict(shipping) for shipping in shippings]
    
    return jsonify(customer_details)

if __name__ == '__main__':
    app.run(debug=True)
