-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS matches;

DROP TABLE IF EXISTS players;

CREATE TABLE players (id SERIAL PRIMARY KEY, name TEXT, wins INT DEFAULT 0, matches INT DEFAULT 0);

CREATE TABLE matches (id SERIAL PRIMARY KEY, winner_id INT, loser_id INT, FOREIGN KEY (winner_id) REFERENCES players (id), FOREIGN KEY (loser_id) REFERENCES players (id));