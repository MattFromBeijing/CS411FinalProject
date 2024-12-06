-- Drop the table if it already exists
DROP TABLE IF EXISTS logs;

-- Create the logs table
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    muscle_group INTEGER NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES login (id)
);