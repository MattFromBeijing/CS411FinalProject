-- Drop the table if it already exists
DROP TABLE IF EXISTS login;

-- Create the login table
CREATE TABLE login (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each user
    username TEXT NOT NULL UNIQUE, -- Unique username
    salt TEXT NOT NULL, -- Salt for password hashing
    hashed_password TEXT NOT NULL, -- Securely hashed password
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for account creation
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for last password update
);