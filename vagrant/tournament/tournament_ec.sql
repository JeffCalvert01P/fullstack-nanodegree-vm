-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- CREATE DATABASE tournament;

\c tournament

DROP VIEW IF EXISTS matches_count_view;
DROP TABLE IF EXISTS matches_table;
DROP TABLE IF EXISTS player_table;

CREATE TABLE player_table (
	tournament 		integer,
	unique_player_id 	SERIAL PRIMARY KEY,
	player_name 	VARCHAR(80),
	wins 			INTEGER,
	matches		 	INTEGER,
	last_result  	VARCHAR(1)
 );
-- COMMIT;
 
CREATE TABLE matches_table (
	unique_match_id 	SERIAL,
	tournament 	 		integer,
	player1_id 			INTEGER REFERENCES player_table(unique_player_id),
	player2_id		 	INTEGER REFERENCES player_table(unique_player_id),	
	winner_id 			INTEGER REFERENCES player_table (unique_player_id),
	round_num 			INTEGER,
	tie_ind 			VARCHAR(1),
	primary key (tournament, player1_id, player2_id)
	);
-- COMMIT;


-- Create view to show competitor match count
create view matches_count_view as (select a.unique_player_id, count(b.unique_match_id) from player_table a, matches_table b where (player1_id = a.unique_player_id or player2_id = a.unique_player_id) and winner_id <> a.unique_player_id group by a.unique_player_id order by a.unique_player_id);
	
 
 
