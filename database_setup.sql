-- Hotel Audit Platform - MS SQL Server Database Setup Script
-- Run this script on your local MS SQL Server instance

-- Create the database (optional - modify database name as needed)
-- CREATE DATABASE hotel_audit_db;
-- USE hotel_audit_db;

-- ========================================
-- CREATE TABLES
-- ========================================

-- Create users table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(255) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL,
    role NVARCHAR(50) NOT NULL,
    name NVARCHAR(255) NOT NULL,
    email NVARCHAR(255) NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Create hotel_groups table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='hotel_groups' AND xtype='U')
CREATE TABLE hotel_groups (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL UNIQUE,
    sop NTEXT,
    sop_files NTEXT,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE()
);

-- Create properties table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='properties' AND xtype='U')
CREATE TABLE properties (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    location NVARCHAR(255) NOT NULL,
    region NVARCHAR(255) NOT NULL,
    hotel_group_id INT FOREIGN KEY REFERENCES hotel_groups(id),
    image NVARCHAR(500),
    last_audit_score INT,
    next_audit_date DATETIME2,
    status NVARCHAR(50) DEFAULT 'green',
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Create audits table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='audits' AND xtype='U')
CREATE TABLE audits (
    id INT IDENTITY(1,1) PRIMARY KEY,
    property_id INT NOT NULL FOREIGN KEY REFERENCES properties(id),
    auditor_id INT FOREIGN KEY REFERENCES users(id),
    reviewer_id INT FOREIGN KEY REFERENCES users(id),
    hotel_group_id INT FOREIGN KEY REFERENCES hotel_groups(id),
    sop NTEXT,
    sop_files NTEXT,
    status NVARCHAR(50) DEFAULT 'scheduled',
    overall_score INT,
    cleanliness_score INT,
    branding_score INT,
    operational_score INT,
    compliance_zone NVARCHAR(50),
    findings NTEXT,
    action_plan NTEXT,
    submitted_at DATETIME2,
    reviewed_at DATETIME2,
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Create audit_items table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='audit_items' AND xtype='U')
CREATE TABLE audit_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    audit_id INT NOT NULL FOREIGN KEY REFERENCES audits(id),
    category NVARCHAR(255) NOT NULL,
    item NTEXT NOT NULL,
    score INT,
    comments NTEXT,
    ai_analysis NTEXT,
    photos NTEXT,
    status NVARCHAR(50) DEFAULT 'pending'
);

-- ========================================
-- INSERT DEMO DATA
-- ========================================

-- Insert demo users (5 roles: admin, auditor, reviewer, corporate, hotelgm)
INSERT INTO users (username, password, role, name, email) VALUES
('admin', 'password', 'admin', 'Admin User', 'admin@hotel.com'),
('auditor', 'password', 'auditor', 'Sarah Johnson', 'sarah.johnson@audit.com'),
('reviewer', 'password', 'reviewer', 'Michael Chen', 'michael.chen@qa.com'),
('corporate', 'password', 'corporate', 'Corporate User', 'corporate@hotel.com'),
('hotelgm', 'password', 'hotelgm', 'Hotel GM', 'gm@tajpalace.com');

-- Insert hotel groups with comprehensive SOPs
INSERT INTO hotel_groups (name, sop, sop_files) VALUES 
(
    'Taj Hotels', 
    '{"brandStandards":{"cleanliness":{"housekeeping":"Rooms must be cleaned to white-glove standards with daily quality checks","publicAreas":"All public areas cleaned hourly, marble surfaces polished twice daily","restaurants":"Kitchen deep cleaning after each service, dining areas sanitized between guests"},"branding":{"signage":"All Taj branding must be prominently displayed with proper lighting","uniforms":"Staff uniforms must be pristine with proper name tags and accessories","ambiance":"Maintain luxury Indian hospitality ambiance with traditional elements"},"service":{"responseTime":"Guest requests acknowledged within 2 minutes, resolved within 10 minutes","greeting":"Traditional Indian greeting Namaste with hands folded","concierge":"24/7 concierge service with local expertise and cultural knowledge"}},"scoringCriteria":{"excellent":"90-100: Exceeds Taj luxury standards significantly","good":"80-89: Meets most Taj standards with minor gaps","acceptable":"70-79: Basic Taj standards met, improvement needed","poor":"Below 70: Immediate corrective action required"}}',
    '[{"name":"Taj_Brand_Standards_2024.pdf","type":"application/pdf","size":2450000,"url":"/uploads/sop/taj-brand-standards-2024.pdf","uploadedAt":"2025-01-24T12:00:00.000Z"},{"name":"Taj_Service_Excellence_Guide.docx","type":"application/vnd.openxmlformats-officedocument.wordprocessingml.document","size":1200000,"url":"/uploads/sop/taj-service-excellence-guide.docx","uploadedAt":"2025-01-24T12:00:00.000Z"}]'
),
(
    'Marriott International', 
    '{"brandStandards":{"cleanliness":{"housekeeping":"Marriott Clean standards with enhanced sanitization protocols","publicAreas":"High-touch surfaces sanitized every 30 minutes","restaurants":"Food safety protocols strictly followed with temperature monitoring"},"branding":{"signage":"Marriott branding consistent across all touchpoints","uniforms":"Professional business attire with Marriott badges","technology":"Mobile check-in/out capabilities fully functional"},"service":{"responseTime":"Guest requests handled within 5 minutes","greeting":"Warm professional greeting with eye contact","loyalty":"Marriott Bonvoy benefits properly communicated and delivered"}},"scoringCriteria":{"excellent":"90-100: Exceptional Marriott service delivery","good":"80-89: Solid Marriott standards compliance","acceptable":"70-79: Meets basic requirements, room for improvement","poor":"Below 70: Does not meet Marriott brand standards"}}',
    '[{"name":"Marriott_Operations_Manual.pdf","type":"application/pdf","size":3200000,"url":"/uploads/sop/marriott-operations-manual.pdf","uploadedAt":"2025-01-24T12:00:00.000Z"}]'
),
(
    'Hilton Worldwide', 
    '{"brandStandards":{"cleanliness":{"housekeeping":"CleanStay standards with hospital-grade disinfection","publicAreas":"Electrostatic spraying in high-traffic areas","restaurants":"Enhanced food safety with contactless service options"},"branding":{"signage":"Hilton branding visible and well-lit at all entry points","uniforms":"Contemporary professional attire with Hilton logos","technology":"Digital key technology fully implemented"},"service":{"responseTime":"Guest requests acknowledged immediately, resolved within 3 minutes","greeting":"Friendly welcome with genuine hospitality","honors":"Hilton Honors benefits clearly explained and delivered"}},"scoringCriteria":{"excellent":"90-100: Outstanding Hilton hospitality standards","good":"80-89: Strong compliance with Hilton expectations","acceptable":"70-79: Adequate performance with improvement areas","poor":"Below 70: Significant gaps in Hilton brand delivery"}}',
    '[{"name":"Hilton_Brand_Standards_Guide.pdf","type":"application/pdf","size":2800000,"url":"/uploads/sop/hilton-brand-standards-guide.pdf","uploadedAt":"2025-01-24T12:00:00.000Z"}]'
);

-- Insert demo properties
INSERT INTO properties (name, location, region, hotel_group_id, image, last_audit_score, next_audit_date, status) VALUES
('Taj Palace, New Delhi', 'New Delhi', 'North India', 1, 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300', 85, DATEADD(day, 30, GETDATE()), 'green'),
('Taj Mahal, Mumbai', 'Mumbai', 'West India', 1, 'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300', 72, DATEADD(day, 15, GETDATE()), 'amber'),
('Taj Lake Palace, Udaipur', 'Udaipur', 'North India', 1, 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300', 92, DATEADD(day, 45, GETDATE()), 'green'),
('Marriott Grand, Goa', 'Goa', 'West India', 2, 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300', 78, DATEADD(day, 20, GETDATE()), 'amber'),
('Hilton Garden Inn, Bangalore', 'Bangalore', 'South India', 3, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300', 81, DATEADD(day, 25, GETDATE()), 'green');

-- Insert demo audits with various statuses
INSERT INTO audits (property_id, auditor_id, reviewer_id, hotel_group_id, status, overall_score, cleanliness_score, branding_score, operational_score, compliance_zone, findings, action_plan, submitted_at, reviewed_at) VALUES
(
    1, 2, 3, 1, 'completed', 88, 90, 85, 90, 'green',
    'Comprehensive audit completed. Property demonstrates excellent adherence to Taj luxury standards with exceptional cleanliness protocols and guest service delivery. Minor areas for improvement identified in branding consistency.',
    '1. Review brand signage placement in lobby area
2. Ensure all staff uniforms meet pristine standards
3. Continue excellence in housekeeping protocols
4. Maintain high service response times
5. Schedule follow-up review in 90 days',
    DATEADD(day, -5, GETDATE()),
    DATEADD(day, -2, GETDATE())
),
(
    2, 2, 3, 1, 'submitted', 85, 88, 80, 87, 'green',
    'Audit submitted for review. Property shows good compliance with Taj standards. Some improvement opportunities identified in branding elements and operational efficiency.',
    '1. Update branding materials to current Taj guidelines
2. Enhance staff training on service protocols
3. Review cleaning procedures for consistency
4. Implement guest feedback system improvements
5. Focus on maintaining high cleanliness standards',
    DATEADD(day, -1, GETDATE()),
    NULL
),
(
    3, 2, NULL, 1, 'in_progress', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
),
(
    4, 2, NULL, 2, 'scheduled', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
),
(
    5, 2, NULL, 3, 'scheduled', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
);

-- Insert detailed audit items for completed audits
INSERT INTO audit_items (audit_id, category, item, score, comments, ai_analysis, photos, status) VALUES
-- Audit ID 1 (Taj Palace Delhi - Completed)
(1, 'Cleanliness', 'Lobby cleanliness and maintenance standards', 4, 'Excellent cleanliness throughout lobby area. Marble surfaces well-maintained and polished.', 'Outstanding performance in lobby cleanliness with attention to detail. Marble surfaces show professional maintenance. Recommend maintaining current standards.', '[]', 'completed'),
(1, 'Cleanliness', 'Guest room housekeeping standards', 5, 'Impeccable room preparation with white-glove cleaning standards met consistently.', 'Exceptional housekeeping standards demonstrated. All surfaces thoroughly cleaned and sanitized. Towels and linens perfectly arranged. Exceeds Taj luxury expectations.', '[]', 'completed'),
(1, 'Branding', 'Taj logo placement and visibility', 3, 'Some inconsistencies in logo placement around property perimeter.', 'Moderate compliance with brand guidelines. Main signage excellent, but secondary locations need attention. Several placement inconsistencies require standardization.', '[]', 'completed'),
(1, 'Branding', 'Staff uniform compliance and presentation', 4, 'Staff uniforms generally excellent with minor attention needed to accessories.', 'Strong uniform compliance overall. Professional appearance maintained by majority of staff. Minor improvements needed in accessory consistency and name tag placement.', '[]', 'completed'),
(1, 'Operational', 'Front desk service efficiency', 5, 'Outstanding guest service with response times consistently under 2 minutes.', 'Exceptional front desk performance. Guest requests handled promptly and professionally. Traditional Namaste greeting properly implemented. Service excellence maintained throughout observation period.', '[]', 'completed'),
(1, 'Operational', 'Concierge service quality', 4, 'Excellent local knowledge and cultural expertise demonstrated by concierge team.', 'Strong concierge performance with comprehensive local knowledge. Cultural recommendations appropriate and well-informed. Response time excellent. Maintain current service levels.', '[]', 'completed'),

-- Audit ID 2 (Taj Mahal Mumbai - Submitted)
(2, 'Cleanliness', 'Restaurant dining area cleanliness', 4, 'Dining areas well-maintained with proper sanitization between guests.', 'Good cleanliness standards in restaurant areas. Sanitization protocols properly followed. Tables properly cleaned between seatings. Maintain current procedures.', '[]', 'completed'),
(2, 'Cleanliness', 'Public restroom maintenance', 3, 'Restrooms clean but some areas need more frequent attention throughout the day.', 'Adequate restroom maintenance with room for improvement. Basic cleanliness standards met but frequency of cleaning could be increased during peak hours.', '[]', 'completed'),
(2, 'Branding', 'Taj branding consistency in restaurant areas', 2, 'Branding materials need updating to current Taj guidelines and standards.', 'Below standard brand consistency. Several branding elements outdated or inconsistent with current Taj guidelines. Immediate attention required for brand compliance.', '[]', 'completed'),
(2, 'Operational', 'Restaurant service timing and quality', 4, 'Good service quality with friendly staff and reasonable response times.', 'Solid operational performance in restaurant service. Staff friendly and knowledgeable. Service timing meets expectations. Continue current training programs.', '[]', 'completed');

-- ========================================
-- VERIFICATION QUERIES
-- ========================================

-- Verify data insertion
PRINT 'Database setup completed successfully!';
PRINT '';
PRINT 'Data Summary:';
SELECT 'Users' as TableName, COUNT(*) as RecordCount FROM users
UNION ALL
SELECT 'Hotel Groups', COUNT(*) FROM hotel_groups
UNION ALL
SELECT 'Properties', COUNT(*) FROM properties
UNION ALL
SELECT 'Audits', COUNT(*) FROM audits
UNION ALL
SELECT 'Audit Items', COUNT(*) FROM audit_items;

PRINT '';
PRINT 'Demo Login Credentials:';
PRINT 'Admin: admin/password';
PRINT 'Auditor: auditor/password';
PRINT 'Reviewer: reviewer/password';
PRINT 'Corporate: corporate/password';
PRINT 'Hotel GM: hotelgm/password';