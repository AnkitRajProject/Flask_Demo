import sqlite3

# Connect to SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('customers.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create Customers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER,
    country TEXT
)
''')

# Create Orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    amount REAL NOT NULL,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
)
''')

# Create Shippings table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Shippings (
    shipping_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL,
    customer INTEGER,
    FOREIGN KEY (customer) REFERENCES Customers(customer_id)
)
''')

# Insert sample data into Customers table
cursor.executemany('''
INSERT INTO Customers (first_name, last_name, age, country) VALUES (?, ?, ?, ?)
''', [
    ('John', 'Doe', 30, 'USA'),
    ('Jane', 'Smith', 25, 'Canada'),
    ('Alice', 'Johnson', 28, 'UK'),
    ('Bob', 'Brown', 35, 'Australia')
])

# Insert sample data into Orders table
cursor.executemany('''
INSERT INTO Orders (item, amount, customer_id) VALUES (?, ?, ?)
''', [
    ('Laptop', 1200.00, 1),
    ('Phone', 800.00, 2),
    ('Tablet', 300.00, 3),
    ('Monitor', 200.00, 4)
])

# Insert sample data into Shippings table
cursor.executemany('''
INSERT INTO Shippings (status, customer) VALUES (?, ?)
''', [
    ('Shipped', 1),
    ('Pending', 2),
    ('Delivered', 3),
    ('In Transit', 4)
])

# Commit the transactions
conn.commit()

# Close the connection
conn.close()

print("Database created and populated successfully.")
