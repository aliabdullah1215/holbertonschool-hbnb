-- =========================
-- TEST CRUD OPERATIONS
-- =========================

-- -------- 1. Test Users --------
-- Insert a new user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES ('11111111-1111-1111-1111-111111111111', 'John', 'Doe', 'john.doe@example.com', '$2b$12$examplehash', FALSE);

-- Select all users
SELECT * FROM users;

-- Update a user
UPDATE users
SET last_name = 'Smith'
WHERE email = 'john.doe@example.com';

-- Delete a user
DELETE FROM users
WHERE email = 'john.doe@example.com';


-- -------- 2. Test Places --------
-- Insert a place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES ('22222222-2222-2222-2222-222222222222', 'Cozy Apartment', 'Nice cozy apartment', 120.00, 40.7128, -74.0060, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

-- Select all places
SELECT * FROM places;

-- Update a place
UPDATE places
SET price = 150.00
WHERE title = 'Cozy Apartment';

-- Delete a place
DELETE FROM places
WHERE title = 'Cozy Apartment';


-- -------- 3. Test Reviews --------
-- Insert a review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES ('33333333-3333-3333-3333-333333333333', 'Great place!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', '22222222-2222-2222-2222-222222222222');

-- Select all reviews
SELECT * FROM reviews;

-- Update a review
UPDATE reviews
SET rating = 4
WHERE id = '33333333-3333-3333-3333-333333333333';

-- Delete a review
DELETE FROM reviews
WHERE id = '33333333-3333-3333-3333-333333333333';


-- -------- 4. Test Amenities --------
-- Insert an amenity
INSERT INTO amenities (id, name)
VALUES ('44444444-4444-4444-4444-444444444444', 'Gym');

-- Select all amenities
SELECT * FROM amenities;

-- Update an amenity
UPDATE amenities
SET name = 'Fitness Center'
WHERE id = '44444444-4444-4444-4444-444444444444';

-- Delete an amenity
DELETE FROM amenities
WHERE id = '44444444-4444-4444-4444-444444444444';


-- -------- 5. Test Place_Amenity --------
-- Link a place with an amenity
INSERT INTO place_amenity (place_id, amenity_id)
VALUES ('22222222-2222-2222-2222-222222222222', 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d');

-- Select all place_amenity links
SELECT * FROM place_amenity;

-- Delete the link
DELETE FROM place_amenity
WHERE place_id = '22222222-2222-2222-2222-222222222222'
  AND amenity_id = 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d';

