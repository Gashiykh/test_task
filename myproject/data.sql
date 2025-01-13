INSERT INTO users_user (
    password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
)
VALUES (
    'pbkdf2_sha256$260000$iDyOYCPMdCXBgUDXVx0meY$jo/WKvUCwG25bKFm9JIdrCINxvQWE3PO0lNqBDlTXXE=',  
    NULL, 
    FALSE, 
    'dev',
    '',  
    '',  
    'dev@example.com',  
    FALSE,  
    TRUE,  
    NOW() 
);

INSERT INTO users_user (
    password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
)
VALUES (
    'pbkdf2_sha256$870000$NwWljo5VCbxJE3Lg2OFtFf$6Kuz47HnmOrV9iTn2M4KHaynu2hpq4QWa/Kx1MILFDw=', 
    NULL,  
    TRUE,  
    'admin',  
    '', 
    '',  
    'admin@example.com', 
    TRUE, 
    TRUE, 
    NOW()  
);

INSERT INTO api_product (name, price)
VALUES
('Bread', 100.00),
('Milk', 150.00),
('Cheese', 200.00),
('Apple', 50.00);


