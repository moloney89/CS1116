DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);


DROP TABLE IF EXISTS events;

CREATE TABLE events
(
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    event_date TEXT NOT NULL,
    event_name TEXT NOT NULL,
    event_start_time TEXT,
    event_end_time TEXT,
    event_category TEXT NOT NULL,
    event_description TEXT
);

DROP TABLE IF EXISTS to_do_list;

CREATE TABLE to_do_list
(
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    item_details TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    completed INTEGER DEFAULT FALSE
);

DROP TABLE IF EXISTS expenses;

CREATE TABLE expenses
(
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    date TEXT NOT NULL,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT DEFAULT 'Miscellaneous',
    details TEXT
);






