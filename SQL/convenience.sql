DROP DATABASE IF EXISTS convenience_store_db;
CREATE DATABASE convenience_store_db;
USE convenience_store_db;

-- 1. Categories Table
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- 2. Locations Table (Aisles & Shelves)
CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    aisle VARCHAR(50) NOT NULL,
    shelf VARCHAR(50) NOT NULL
);

-- 3. Products Table (Full store inventory - 20 per category)
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category_id INT,
    location_id INT,
    price DECIMAL(10,2) NOT NULL,
    stock_qty INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- 4. Employees Table
CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'Staff'
);

-- Insert Categories
INSERT INTO categories (category_name) VALUES 
('Biscuits'), ('Grocery'), ('Non-Food'), ('Confectionery'), ('Chips');

-- Insert Locations
INSERT INTO locations (aisle, shelf) VALUES 
('Aisle 1', 'Shelf A-1'), 
('Aisle 2', 'Shelf B-2'), 
('Aisle 3', 'Shelf C-3'),
('Aisle 4', 'Shelf D-4');

-- Insert 20 Products per Category (100 Total)
INSERT INTO products (name, category_id, location_id, price, stock_qty) VALUES 
-- Biscuits (Category ID: 1)
('SkyFlakes Crackers', 1, 1, 15.00, 100),
('Fita Crackers', 1, 1, 16.50, 85),
('Rebisco Crackers', 1, 1, 10.00, 120),
('Magic Flakes', 1, 1, 10.00, 110),
('Cream-O Cookies', 1, 1, 12.00, 95),
('Bingo Cookie Butter', 1, 1, 12.00, 90),
('Hansel Mocha Sandwich', 1, 1, 11.00, 105),
('Fibisco Chocolate Chip', 1, 2, 45.00, 60),
('Eggnog Cookies', 1, 2, 35.00, 70),
('Marie Biscuits', 1, 2, 25.00, 80),
('Nissin Butter Coconut', 1, 2, 14.00, 115),
('Nissin Wafers Chocolate', 1, 2, 10.00, 130),
('Voortman Cookies', 1, 2, 85.00, 40),
('Quaker Oatmeal Cookies', 1, 2, 95.00, 45),
('Lemon Square Cheese Cupcake', 1, 2, 12.00, 100),
('Brazo de Mercedes Roll', 1, 2, 35.00, 50),
('San Marino Corned Tuna Bread', 1, 2, 28.00, 65),
('Presto Peanut Butter Sandwich', 1, 2, 11.00, 110),
('M.Y. San Graham Crackers', 1, 2, 58.00, 75),
('Lars Butter Cookies', 1, 2, 110.00, 30),

-- Grocery (Category ID: 2)
('Datu Puti Soy Sauce', 2, 2, 35.00, 50),
('Silver Swan Vinegar', 2, 2, 32.00, 55),
('UFC Banana Ketchup', 2, 2, 45.00, 75),
('Century Tuna', 2, 2, 42.00, 120),
('Lucky Me! Instant Noodles', 2, 2, 11.00, 300),
('Mega Sardines', 2, 2, 25.00, 150),
('San Miguel Butter', 2, 3, 95.00, 40),
('Angel Evaporated Milk', 2, 3, 48.00, 90),
('Dona Maria Rice (1kg)', 2, 3, 85.00, 60),
('Argentina Corned Beef', 2, 3, 38.00, 110),
('Bounty Fresh Eggs (10pcs)', 2, 3, 75.00, 65),
('Magnolia Fresh Milk (1L)', 2, 3, 98.00, 45),
('Nescafe Classic Coffee', 2, 3, 65.00, 80),
('Great Taste White Coffee', 2, 3, 8.00, 250),
('Bear Brand Milk Powder', 2, 3, 90.00, 70),
('Lipton Yellow Label Tea', 2, 3, 120.00, 35),
('Milo Active-Go', 2, 3, 15.00, 180),
('Sunpride Pork Luncheon Meat', 2, 3, 58.00, 85),
('Master Sardines in Tomato Sauce', 2, 3, 24.00, 140),
('Datu Puti Patis', 2, 3, 30.00, 60),

-- Non-Food (Category ID: 3)
('Safeguard Soap', 3, 3, 28.00, 60),
('Creamsilk Conditioner', 3, 3, 90.00, 50),
('Palmolive Shampoo', 3, 3, 85.00, 55),
('Surf Powder Detergent', 3, 3, 40.00, 80),
('Zonrox Bleach', 3, 3, 35.00, 45),
('Joy Dishwashing Liquid', 3, 3, 45.00, 70),
('Unique Toothpaste', 3, 3, 55.00, 65),
('Sanicare Facial Tissue', 3, 3, 65.00, 40),
('Green Cross Alcohol', 3, 3, 75.00, 100),
('Casino Rubbing Alcohol', 3, 3, 78.00, 90),
('Colgate Toothbrush', 3, 3, 45.00, 50),
('Rexona Deodorant Roll-on', 3, 3, 95.00, 40),
('Bioderm Soap', 3, 3, 25.00, 75),
('Head & Shoulders Shampoo', 3, 3, 110.00, 45),
('Downy Fabric Softener Refill', 3, 3, 58.00, 85),
('Master Facial Cleanser', 3, 3, 85.00, 35),
('Kojic San Skin Soap', 3, 3, 60.00, 60),
('Modess Sanitary Napkin', 3, 3, 48.00, 90),
('Cotton Buds Johnson & Johnson', 3, 3, 38.00, 50),
('Off! Insect Repellent Lotion', 3, 3, 98.00, 40),

-- Confectionery (Category ID: 4)
('Flat Tops Chocolates', 4, 1, 55.00, 200),
('Curly Tops Chocolates', 4, 1, 55.00, 180),
('Choc-Nut', 4, 1, 35.00, 250),
('Hany Milk Chocolate', 4, 1, 35.00, 220),
('Potchi Candy', 4, 1, 25.00, 150),
('XO Coffee Candy', 4, 1, 30.00, 130),
('Max''s Menthol Candy', 4, 1, 28.00, 140),
('Stork Candies', 4, 1, 25.00, 160),
('Lala Milk Chocolate', 4, 1, 40.00, 110),
('Frutos Chewy Candy', 4, 1, 26.00, 120),
('Cloud 9 Chocolate Bar', 4, 1, 10.00, 200),
('Nips Milk Chocolate', 4, 1, 15.00, 190),
('Knick Knacks Chocolate', 4, 1, 18.00, 170),
('Hershey''s Milk Chocolate Bar', 4, 2, 75.00, 50),
('Toblerone Swiss Chocolate', 4, 2, 125.00, 40),
('Mentos Mint Roll', 4, 2, 20.00, 130),
('Chupa Chups Lollipop', 4, 2, 8.00, 220),
('Bazooka Bubble Gum', 4, 2, 5.00, 300),
('Judge Bubble Gum', 4, 2, 5.00, 280),
('Meiji Hello Panda', 4, 2, 35.00, 90),

-- Chips (Category ID: 5)
('Piattos Cheese', 5, 1, 22.00, 150),
('Nova Multigrain Chips', 5, 1, 22.00, 140),
('Vcut Potato Chips', 5, 1, 23.00, 130),
('Chippy Barbecue', 5, 1, 18.00, 170),
('Oishi Prawn Crackers', 5, 1, 17.00, 160),
('Roller Coaster', 5, 1, 20.00, 110),
('Ding Dong Mixed Nuts', 5, 2, 35.00, 90),
('Nagaraya Nuts', 5, 2, 38.00, 85),
('Clover Chips', 5, 2, 19.00, 145),
('Boy Bawang Garlic', 5, 2, 16.00, 190),
('Oishi Sponge Crunch', 5, 2, 15.00, 135),
('Mr. Chips Cheese', 5, 2, 18.00, 155),
('Jack ''n Jill Tortillos', 5, 2, 21.00, 120),
('Tostitos Tortilla Chips', 5, 4, 115.00, 30),
('Pringles Original', 5, 4, 95.00, 50),
('Riggle Potato Chips', 5, 4, 45.00, 70),
('Happy Peanuts Garlic', 5, 4, 15.00, 200),
('W.L. Food Fish Crackers', 5, 4, 12.00, 180),
('Patatas Potato Crisps', 5, 4, 25.00, 110),
('Snacku Rice Cracker', 5, 4, 10.00, 210);

-- Insert Default Admin Employee
INSERT INTO employees (username, password, role) VALUES ('admin', '1234', 'Manager');