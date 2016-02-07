-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--
--Players
--PlayerId serial primary key | PlayerName text | TournamentId int
--
--Tournament
--TournamentId int | PlayerId int | Wins int | Draws int | Losses int | Round int

CREATE TABLE players
(
PlayerId serial primary key,
PlayerName text
);

CREATE TABLE tournaments
(
TournamentId serial primary key,
PlayerId integer references players(PlayerId),
PlayerName integer references players(PlayerName),
Wins integer,
Losses integer,
Draws integer,
Matches integer
);




