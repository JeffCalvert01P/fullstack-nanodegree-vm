-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.




-- CREATE DATABASE tournament;

\c tournament

DROP TABLE IF EXISTS matches_table;
DROP TABLE IF EXISTS player_table;

CREATE TABLE player_table (
	unique_player_id 	SERIAL PRIMARY KEY,
	player_name 	VARCHAR(80),
	wins 			INTEGER,
	matches		 	INTEGER
 );
-- COMMIT;
 
CREATE TABLE matches_table (
	unique_match_id 	SERIAL,
	player1_id 			INTEGER REFERENCES player_table(unique_player_id),
	player2_id		 	INTEGER REFERENCES player_table(unique_player_id),	
	primary key (player1_id, player2_id)
	);
-- COMMIT;


	
 
 
