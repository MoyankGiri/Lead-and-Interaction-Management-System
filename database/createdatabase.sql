-- Create Leads Table
CREATE TABLE Leads (
    lead_id SERIAL PRIMARY KEY,
    restaurant_name VARCHAR(255) NOT NULL,
    address TEXT,
    status VARCHAR(50) CHECK (status IN ('New', 'Active', 'Closed')),
    call_frequency INT CHECK (call_frequency >= 0),
    last_call_date DATE
);

-- Create Points of Contact (POCs) Table
CREATE TABLE POCs (
    poc_id SERIAL PRIMARY KEY,
    lead_id INT REFERENCES Leads(lead_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(255)
);

-- Create Interactions Table
CREATE TABLE Interactions (
    interaction_id SERIAL PRIMARY KEY,
    lead_id INT REFERENCES Leads(lead_id) ON DELETE CASCADE,
    interaction_date DATE NOT NULL,
    details TEXT,
    order_placed BOOLEAN DEFAULT FALSE
);

-- Create Performance Metrics Table
CREATE TABLE PerformanceMetrics (
    performance_id SERIAL PRIMARY KEY,
    lead_id INT REFERENCES Leads(lead_id) ON DELETE CASCADE,
    order_frequency INT CHECK (order_frequency >= 0),
    last_order_date DATE,
    performance_status VARCHAR(50) CHECK (performance_status IN ('Well-performing', 'Underperforming'))
);

-- Insert into Leads
INSERT INTO Leads (restaurant_name, address, status, call_frequency, last_call_date)
VALUES 
('Taco Town', '321 Maple St, Rivertown', 'Active', 8, '2024-12-22'),
('Pasta Palace', '654 Pine St, Rivertown', 'Active', 6, '2024-12-18'),
('Steakhouse Supreme', '987 Birch St, Rivertown', 'Active', 2, '2024-11-05'),
('Vegan Delight', '135 Cedar St, Rivertown', 'New', 1, NULL),
('BBQ Kings', '246 Willow St, Rivertown', 'Active', 3, '2024-11-20'),
('Dessert Haven', '369 Cherry St, Rivertown', 'Active', 9, '2024-12-14'),
('Sushi Express', '258 Pine St, Rivertown', 'New', 0, NULL),
('Curry Corner', '147 Oak St, Rivertown', 'Active', 4, '2024-12-01'),
('Ramen Rush', '258 Elm St, Rivertown', 'Active', 10, '2024-12-19');

-- Insert into POCs
INSERT INTO POCs (lead_id, name, role, phone, email)
VALUES 
(4, 'David Wilson', 'Owner', '555-1122', 'david@vegandelight.com'),
(5, 'Emma Davis', 'Manager', '555-3344', 'emma@bbqkings.com'),
(6, 'Olivia Harris', 'Owner', '555-5566', 'olivia@desserthaven.com'),
(7, 'Liam Clark', 'Manager', '555-7788', 'liam@sushiexpress.com'),
(8, 'Sophia Martinez', 'Owner', '555-9900', 'sophia@currycorners.com'),
(9, 'James Lee', 'Manager', '555-2233', 'james@ramenrush.com');

-- Insert into Interactions
INSERT INTO Interactions (lead_id, interaction_date, details, order_placed)
VALUES 
(1, '2024-12-21', 'Discussed menu updates and promotions.', TRUE),
(2, '2024-12-18', 'Followed up on marketing materials.', TRUE),
(3, '2024-11-01', 'Discussed sales performance and next steps.', FALSE),
(4, '2024-12-15', 'Introduced lead to seasonal menu items.', FALSE),
(5, '2024-11-19', 'Offered special discounts.', TRUE),
(6, '2024-12-12', 'Talked about upcoming holiday promotions.', TRUE),
(7, '2024-12-05', 'Answered leads queries about the menu.', FALSE),
(8, '2024-11-30', 'Discussed catering services for events.', TRUE),
(9, '2024-12-18', 'Followed up on outstanding payment.', TRUE);

-- Insert into Performance Metrics
INSERT INTO PerformanceMetrics (lead_id, order_frequency, last_order_date, performance_status)
VALUES 
(1, 6, '2024-12-20', 'Well-performing'),
(2, 8, '2024-12-15', 'Well-performing'),
(3, 1, '2024-11-05', 'Underperforming'),
(4, 0, NULL, 'Underperforming'),
(5, 4, '2024-11-20', 'Average'),
(6, 7, '2024-12-10', 'Well-performing'),
(7, 0, NULL, 'Underperforming'),
(8, 3, '2024-11-30', 'Average'),
(9, 9, '2024-12-19', 'Well-performing');