DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS admins;

CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    token TEXT NOT NULL UNIQUE
);

CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    contact TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    address TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    country TEXT NOT NULL,
    passport_number TEXT NOT NULL,
    issuing_country TEXT NOT NULL,
    date_of_issue TEXT NOT NULL,
    date_of_expiration TEXT NOT NULL,
    terms_accepted BOOLEAN NOT NULL,
    signature TEXT,
    group_id INTEGER,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
);