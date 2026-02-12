-- 1. تنظيف شامل للبيانات القديمة
DELETE FROM reviews;
DELETE FROM places;
DELETE FROM amenities;
DELETE FROM users;

-- 2. حقن المستخدمين (مع تمرير الوقت CURRENT_TIMESTAMP)
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES 
('u-admin', 'Ali', 'Abdullah', 'admin@hbnb.com', 'pass_admin', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('u-host-1', 'Sami', 'Khalid', 'sami@host.com', 'pass_host', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('u-guest-1', 'Sara', 'Ahmed', 'sara@guest.com', 'pass_guest', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 3. حقن المرافق
INSERT INTO amenities (id, name, created_at, updated_at) VALUES 
('a1', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP), 
('a2', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP), 
('a3', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 4. حقن الأماكن
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at) VALUES 
('p1', 'Modern Apartment', 'Near city center', 120.00, 24.71, 46.67, 'u-host-1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('p2', 'Desert Resort', 'Quiet and peaceful', 350.00, 24.85, 46.50, 'u-host-1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 5. حقن التقييمات
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at) VALUES 
('r1', 'Clean and tidy!', 5, 'u-guest-1', 'p1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('r2', 'A bit far from shops', 3, 'u-guest-1', 'p2', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
