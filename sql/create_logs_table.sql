-- Drop the table if it already exists
DROP TABLE IF EXISTS logs;

-- Create the logs table
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    exercise_name TEXT NOT NULL,
    muscle_groups TEXT NOT NULL,
    date TEXT NOT NULL UNIQUE,
    FOREIGN KEY (username) REFERENCES login (username)
);