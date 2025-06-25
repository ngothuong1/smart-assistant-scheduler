-- DROP TABLE users
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(30) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    avatar TEXT NULL,
    email VARCHAR(100) NOT NULL
);

-- DROP TABLE users_token
CREATE TABLE IF NOT EXISTS users_token (
    user_id VARCHAR(30) PRIMARY KEY,
    google_token JSON NULL,
    google_history_id VARCHAR(30) NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);