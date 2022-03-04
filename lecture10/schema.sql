DROP TABLE IF EXISTS votes;

CREATE TABLE votes
(
    number INTEGER PRIMARY KEY,
    total_votes INTEGER NOT NULL
);

INSERT INTO votes (number, total_votes)
VALUES (0, 0), (1,0)