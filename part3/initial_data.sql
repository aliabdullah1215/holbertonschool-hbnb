-- تنظيف البيانات القديمة لضمان بداية نظيفة (اختياري)
DELETE FROM place_amenity;
DELETE FROM reviews;
DELETE FROM places;
DELETE FROM amenities;
DELETE FROM users;

-- 1. حقن مستخدم أدمن (Admin)
-- المعرف (ID) هو UUID ثابت لكي نتمكن من استخدامه في ربط الجداول الأخرى
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES ('user-admin-001', 'Ali', 'Abdullah', 'admin@hbnb.com', 'password123', 1);

-- 2. حقن المرافق (Amenities)
INSERT INTO amenities (id, name) VALUES 
('am-001', 'WiFi'), 
('am-002', 'Swimming Pool'), 
('am-003', 'Air Conditioning');

-- 3. حقن مكان (Place) مملوك للأدمن
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES ('pl-001', 'Luxury Riyadh Villa', 'A beautiful villa with sunset view', 450.00, 24.7136, 46.6753, 'user-admin-001');

-- 4. ربط المكان بالمرافق (Many-to-Many)
INSERT INTO place_amenity (place_id, amenity_id) VALUES 
('pl-001', 'am-001'),
('pl-001', 'am-003');

-- 5. حقن تقييم (Review) للمكان
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES ('rev-001', 'Amazing place, very clean!', 5, 'user-admin-001', 'pl-001');
