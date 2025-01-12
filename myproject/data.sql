INSERT INTO users_user (
    password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
)
VALUES (
    'pbkdf2_sha256$600000$q0FGV4E3psFkBfxgRL9O$S5h6zJeqUGSTKvVzJeUPDe+jkjLS0GboBDwle7FS/5s=',  -- хэш пароля "user"
    NULL, 
    FALSE, 
    'user',
    '',  
    '',  
    'user@example.com',  
    FALSE,  
    TRUE,  
    NOW() 
);

INSERT INTO users_user (
    password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
)
VALUES (
    'pbkdf2_sha256$600000$O0oJLFqeGs5UwlBk0oXk$zHgZqBP6dXZfPtH9xkLBxMSkEm6mA+yDjC3S0K7G0Jg=',  -- хэш пароля "admin"
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


