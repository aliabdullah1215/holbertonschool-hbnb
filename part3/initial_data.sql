-- =========================
-- Insert Administrator User
-- =========================
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$V8e5oFJfD2F6XH0yHkT6LO1gC0B1tHkKXWc5OZbHkL6lI7n9qT5q6', -- مثال hash bcrypt لكلمة admin1234
    TRUE
);

-- =========================
-- Insert Initial Amenities
-- =========================
INSERT INTO amenities (id, name) VALUES
('a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d', 'WiFi'),
('b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e', 'Swimming Pool'),
('c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f', 'Air Conditioning');
