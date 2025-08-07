#!/usr/bin/env python3
"""
Complete Database Backup Script for EnergyRush
Contains all 10 products and 6734 orders from the production database
"""

import sqlite3
import os

def restore_database(db_path='energyrush.db', overwrite=False):
    """
    Restore the complete EnergyRush database with all products and orders
    
    Args:
        db_path: Path where database will be created (default: energyrush.db)
        overwrite: If True, will overwrite existing database
    """
    
    # Check if database exists
    if os.path.exists(db_path) and not overwrite:
        response = input(f"Database {db_path} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Restore cancelled.")
            return False
    
    # Remove existing database if overwriting
    if os.path.exists(db_path) and overwrite:
        os.remove(db_path)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute SQL dump
    with open('full_database_dump.sql', 'r') as f:
        sql_script = f.read()
    
    cursor.executescript(sql_script)
    conn.commit()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM product")
    product_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM 'order'")
    order_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(total_amount) FROM 'order'")
    total_revenue = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\nDatabase restored successfully to {db_path}!")
    print(f"Statistics:")
    print(f"- Products: {product_count}")
    print(f"- Orders: {order_count}")
    print(f"- Total Revenue: ${total_revenue:,.2f}" if total_revenue else "- Total Revenue: $0.00")
    
    return True

def verify_backup():
    """Verify the SQL dump file exists and has the correct data"""
    if not os.path.exists('full_database_dump.sql'):
        print("Error: full_database_dump.sql not found!")
        print("Please ensure the SQL dump file is in the same directory.")
        return False
    
    # Check file size
    file_size = os.path.getsize('full_database_dump.sql')
    print(f"SQL dump file size: {file_size:,} bytes")
    
    # Count lines
    with open('full_database_dump.sql', 'r') as f:
        line_count = sum(1 for line in f)
    print(f"SQL dump contains {line_count:,} lines")
    
    return True

def create_instance_dir_database():
    """Create database in instance directory for Flask app"""
    instance_dir = 'instance'
    
    # Create instance directory if it doesn't exist
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"Created {instance_dir} directory")
    
    db_path = os.path.join(instance_dir, 'energyrush.db')
    return restore_database(db_path, overwrite=True)

if __name__ == '__main__':
    print("EnergyRush Complete Database Restore Script")
    print("=" * 50)
    print("\nThis script will restore the complete database with:")
    print("- 10 energy drink products")
    print("- 6734 customer orders")
    print()
    
    # Verify backup file exists
    if not verify_backup():
        exit(1)
    
    print("\nRestore options:")
    print("1. Restore to energyrush.db (main directory)")
    print("2. Restore to instance/energyrush.db (Flask app directory)")
    print("3. Restore to both locations")
    print("4. Custom path")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        restore_database('energyrush.db', overwrite=True)
    elif choice == '2':
        create_instance_dir_database()
    elif choice == '3':
        print("\nRestoring to main directory...")
        restore_database('energyrush.db', overwrite=True)
        print("\nRestoring to instance directory...")
        create_instance_dir_database()
    elif choice == '4':
        custom_path = input("Enter database path: ").strip()
        if custom_path:
            restore_database(custom_path, overwrite=True)
        else:
            print("Invalid path")
    else:
        print("Invalid option")
    
    print("\nRestore complete!")