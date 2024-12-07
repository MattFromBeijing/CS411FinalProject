-- Drop the table if it already exists
DROP TABLE IF EXISTS logs;

-- Create the logs table
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercise_name TEXT NOT NULL,
    muscle_group INTEGER NOT NULL,
    date TEXT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES login (id)
);