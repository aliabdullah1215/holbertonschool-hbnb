-- تنظيف البيانات (Ali موجود حالياً، لذا سنمسحه ونعيد تنظيمه)
DELETE FROM users;

-- حقن المستخدمين (بدون ذكر أعمدة الوقت)
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES 
('u-admin', 'Ali', 'Abdullah', 'admin@hbnb.com', 'pass_admin', 1),
('u-host-1', 'Sami', 'Khalid', 'sami@host.com', 'pass_host', 0);

-- حقن المرافق
INSERT INTO amenities (id, name) VALUES 
('a1', 'WiFi'), 
('a2', 'Pool');
