-- Table definitions for the tournament project.
--
-- Put your SQL "create table" statements in this file; also "create view"
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- psql

-- => CREATE DATABASE tournament;

-- => \c tournament

-- => \i tournament.sql

-- Creates a table tournament which is just a bunch of different tournament IDs

CREATE TABLE "tournament" (id serial primary key);

-- Creates the player table, with a primary key ID, name, and timestamp of player creation

CREATE TABLE "player"     (id serial primary key,
                          name varchar(25) not null,
                          tournament_id int,
                          date_created timestamp default current_timestamp,
                          foreign key (tournament_id) references tournament(id));

-- Creates a match. A match can be tied to a different tournament, and it contains a winner and a loser

CREATE TABLE "match"      (id serial primary key,
                          tournament_id int,
                          winner int,
                          loser int,
                          foreign key (tournament_id) references tournament(id),
                          foreign key (winner) references player(id),
                          foreign key (loser) references player(id));

-- View that returns the number of wins that a player has

CREATE VIEW wins as       SELECT player.id, player.name, count(match.id) AS wins
                          FROM player LEFT JOIN match
                          ON player.id = match.winner
                          GROUP BY player.id
                          ORDER BY wins DESC;

-- View that returns the number of losses that a player has

CREATE VIEW losses as     SELECT player.id, player.name, count(match.id) AS losses
                          FROM player LEFT JOIN match
                          ON player.id = match.loser
                          GROUP BY player.id
                          ORDER BY losses DESC;
