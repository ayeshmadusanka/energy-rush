#!/usr/bin/env python3
"""
Database Dump and Restore Script for EnergyRush
This script creates the database schema and inserts sample data
"""

import sqlite3
from datetime import datetime, timedelta
import json
import random

def create_database(db_path='energyrush.db'):
    """Create database schema and insert sample data"""
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS 'order'")
    cursor.execute("DROP TABLE IF EXISTS product")
    
    # Create Product table
    cursor.execute("""
    CREATE TABLE product (
        id INTEGER NOT NULL,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        price FLOAT NOT NULL,
        stock INTEGER NOT NULL,
        image_url VARCHAR(200),
        created_at DATETIME,
        PRIMARY KEY (id)
    )
    """)
    
    # Create Order table
    cursor.execute("""
    CREATE TABLE 'order' (
        id INTEGER NOT NULL,
        customer_name VARCHAR(100) NOT NULL,
        customer_email VARCHAR(100) NOT NULL,
        customer_phone VARCHAR(20),
        customer_address TEXT,
        items TEXT NOT NULL,
        total FLOAT NOT NULL,
        status VARCHAR(20),
        created_at DATETIME,
        PRIMARY KEY (id)
    )
    """)
    
    # Insert sample products
    products = [
        ('Thunder Bolt', 'High-intensity energy drink with electrolytes and B-vitamins', 3.99, 100, 'https://picsum.photos/300/300?random=1'),
        ('Electric Storm', 'Tropical flavored energy boost with guarana and ginseng', 4.49, 75, 'https://picsum.photos/300/300?random=2'),
        ('Power Surge', 'Sugar-free energy drink with green tea extract', 3.49, 150, 'https://picsum.photos/300/300?random=3'),
        ('Nitro Rush', 'Extra caffeine formula for maximum alertness', 4.99, 50, 'https://picsum.photos/300/300?random=4'),
        ('Quantum Leap', 'Natural energy blend with organic ingredients', 5.49, 80, 'https://picsum.photos/300/300?random=5'),
        ('Atomic Blast', 'Classic energy drink with taurine and caffeine', 2.99, 200, 'https://picsum.photos/300/300?random=6')
    ]
    
    created_at = datetime.now()
    for name, description, price, stock, image_url in products:
        cursor.execute("""
            INSERT INTO product (name, description, price, stock, image_url, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, price, stock, image_url, created_at))
    
    # Insert sample orders for ML forecasting
    customer_names = ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Williams', 'Tom Brown', 
                     'Emily Davis', 'Chris Wilson', 'Lisa Anderson', 'David Miller', 'Amy Taylor']
    
    statuses = ['pending', 'processing', 'delivered']
    
    # Generate orders for the last 30 days
    for days_ago in range(30, 0, -1):
        order_date = datetime.now() - timedelta(days=days_ago)
        
        # Generate 5-15 orders per day
        num_orders = random.randint(5, 15)
        
        for _ in range(num_orders):
            # Random customer
            customer_name = random.choice(customer_names)
            customer_email = customer_name.lower().replace(' ', '.') + '@example.com'
            customer_phone = f'+1{random.randint(1000000000, 9999999999)}'
            customer_address = f'{random.randint(100, 999)} Main St, City, State {random.randint(10000, 99999)}'
            
            # Random products (1-3 items per order)
            num_items = random.randint(1, 3)
            order_items = []
            total = 0
            
            selected_products = random.sample(products, num_items)
            for product in selected_products:
                quantity = random.randint(1, 5)
                item = {
                    'product_id': products.index(product) + 1,
                    'name': product[0],
                    'price': product[2],
                    'quantity': quantity
                }
                order_items.append(item)
                total += product[2] * quantity
            
            # Add random time to the date
            order_datetime = order_date + timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            cursor.execute("""
                INSERT INTO 'order' (customer_name, customer_email, customer_phone, 
                                   customer_address, items, total, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (customer_name, customer_email, customer_phone, customer_address,
                  json.dumps(order_items), round(total, 2), random.choice(statuses), order_datetime))
    
    # Commit changes
    conn.commit()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM product")
    product_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM 'order'")
    order_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(total) FROM 'order'")
    total_revenue = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'products': product_count,
        'orders': order_count,
        'total_revenue': round(total_revenue, 2) if total_revenue else 0
    }

def dump_database(db_path='energyrush.db', output_file='database_backup.sql'):
    """Export database to SQL file"""
    conn = sqlite3.connect(db_path)
    
    with open(output_file, 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    
    conn.close()
    print(f"Database dumped to {output_file}")

def restore_database(sql_file='database_backup.sql', db_path='energyrush_restored.db'):
    """Restore database from SQL file"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(sql_file, 'r') as f:
        sql_script = f.read()
    
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print(f"Database restored to {db_path}")

if __name__ == '__main__':
    print("EnergyRush Database Setup Script")
    print("-" * 40)
    
    # Create and populate database
    print("Creating database with sample data...")
    stats = create_database()
    
    print(f"\nDatabase created successfully!")
    print(f"- Products: {stats['products']}")
    print(f"- Orders: {stats['orders']}")
    print(f"- Total Revenue: ${stats['total_revenue']}")
    
    # Optional: Create SQL dump
    print("\nCreating SQL dump...")
    dump_database()
    
    print("\nDatabase setup complete!")
    print("You can now run 'python app.py' to start the application.")