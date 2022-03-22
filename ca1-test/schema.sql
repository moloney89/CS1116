DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);



DROP TABLE IF EXISTS user_details;

CREATE TABLE user_details
(
    user_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
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





