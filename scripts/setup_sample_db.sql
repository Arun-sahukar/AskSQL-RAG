-- AskSQL Sample Database Setup
-- Run this script to create a demo e-commerce database

CREATE DATABASE IF NOT EXISTS asksql_demo;
USE asksql_demo;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS categories;

-- Categories table
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    category_id INT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Customers table
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'USA',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Order items table
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Clothing', 'Apparel and fashion items'),
('Books', 'Books and publications'),
('Home & Garden', 'Home improvement and garden supplies'),
('Sports', 'Sports equipment and accessories');

-- Insert sample products
INSERT INTO products (name, category_id, price, stock_quantity, description) VALUES
('Wireless Headphones', 1, 79.99, 150, 'Bluetooth wireless headphones with noise cancellation'),
('Laptop Stand', 1, 45.99, 200, 'Adjustable aluminum laptop stand'),
('USB-C Hub', 1, 34.99, 300, '7-in-1 USB-C hub with HDMI'),
('Smartphone Case', 1, 19.99, 500, 'Protective case for smartphones'),
('Cotton T-Shirt', 2, 24.99, 400, 'Premium cotton crew neck t-shirt'),
('Denim Jeans', 2, 59.99, 250, 'Classic fit denim jeans'),
('Running Shoes', 2, 89.99, 180, 'Lightweight running shoes'),
('Winter Jacket', 2, 129.99, 100, 'Insulated winter jacket'),
('Python Programming', 3, 49.99, 75, 'Complete guide to Python programming'),
('Data Science Handbook', 3, 39.99, 60, 'Introduction to data science'),
('Garden Tools Set', 4, 54.99, 120, '5-piece garden tool set'),
('Indoor Plant Pot', 4, 22.99, 200, 'Ceramic indoor plant pot'),
('Yoga Mat', 5, 29.99, 180, 'Non-slip yoga mat'),
('Dumbbell Set', 5, 149.99, 50, 'Adjustable dumbbell set 5-50 lbs'),
('Tennis Racket', 5, 79.99, 80, 'Professional tennis racket');

-- Insert sample customers
INSERT INTO customers (first_name, last_name, email, city, state, country) VALUES
('John', 'Smith', 'john.smith@email.com', 'New York', 'NY', 'USA'),
('Sarah', 'Johnson', 'sarah.j@email.com', 'Los Angeles', 'CA', 'USA'),
('Michael', 'Williams', 'mwilliams@email.com', 'Chicago', 'IL', 'USA'),
('Emily', 'Brown', 'emily.b@email.com', 'Houston', 'TX', 'USA'),
('David', 'Jones', 'djones@email.com', 'Phoenix', 'AZ', 'USA'),
('Jessica', 'Davis', 'jdavis@email.com', 'New York', 'NY', 'USA'),
('Daniel', 'Miller', 'dmiller@email.com', 'San Francisco', 'CA', 'USA'),
('Ashley', 'Wilson', 'awilson@email.com', 'Seattle', 'WA', 'USA'),
('James', 'Moore', 'jmoore@email.com', 'Denver', 'CO', 'USA'),
('Amanda', 'Taylor', 'ataylor@email.com', 'Boston', 'MA', 'USA');

-- Insert sample orders
INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES
(1, '2024-01-15 10:30:00', 'delivered', 125.98),
(2, '2024-01-16 14:20:00', 'delivered', 89.99),
(3, '2024-01-17 09:15:00', 'shipped', 184.97),
(4, '2024-01-18 16:45:00', 'processing', 59.99),
(5, '2024-01-19 11:00:00', 'delivered', 79.99),
(6, '2024-01-20 13:30:00', 'shipped', 149.97),
(1, '2024-02-01 10:00:00', 'delivered', 45.99),
(7, '2024-02-05 15:20:00', 'delivered', 269.97),
(8, '2024-02-10 09:45:00', 'processing', 54.99),
(9, '2024-02-15 14:00:00', 'pending', 179.98),
(2, '2024-03-01 11:30:00', 'delivered', 79.98),
(10, '2024-03-05 16:15:00', 'shipped', 129.99);

-- Insert sample order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 79.99),
(1, 4, 2, 19.99),
(2, 7, 1, 89.99),
(3, 5, 2, 24.99),
(3, 6, 1, 59.99),
(3, 13, 2, 29.99),
(4, 6, 1, 59.99),
(5, 1, 1, 79.99),
(6, 9, 1, 49.99),
(6, 10, 1, 39.99),
(6, 5, 2, 24.99),
(7, 2, 1, 45.99),
(8, 8, 1, 129.99),
(8, 14, 1, 149.99),
(9, 11, 1, 54.99),
(10, 15, 1, 79.99),
(10, 13, 2, 29.99),
(11, 1, 1, 79.99),
(12, 8, 1, 129.99);

-- Verify data
SELECT 'Categories' as TableName, COUNT(*) as RowCount FROM categories
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Customers', COUNT(*) FROM customers
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items;
