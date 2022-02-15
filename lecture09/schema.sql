DROP TABLE IF EXISTS gigs;

CREATE TABLE gigs
(
    gig_id INTEGER PRIMARY KEY AUTOINCREMENT,
    band TEXT NOT NULL,
    gig_date TEXT NOT NULL
);

INSERT INTO gigs (band, gig_date)
VALUES  ('Decaying Shroom', '2022-01-12'),
        ('Dumpy Tension of the Divided Unicorn', '2022-02-10'),
        ('Belated Tonic', '2022-01-21'),
        ('Missing Roller and the Earl', '2022-02-26'),
        ('Glam Blizzard', '2022-03-07'),
        ('Piscatory Classroom', '2022-03-12'),
        ('Prickly Muse', '2022-03-20'),
        ('Interactive Children of the Phony Filth', '2022-03-29');

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);