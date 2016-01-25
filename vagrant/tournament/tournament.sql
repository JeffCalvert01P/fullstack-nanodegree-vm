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
DROP VIEW IF EXISTS competitor_count_view;
DROP TABLE IF EXISTS matches_table;
DROP TABLE IF EXISTS player_table;

CREATE TABLE player_table (
	unique_player_id 	SERIAL PRIMARY KEY,
	player_name 	VARCHAR(80)
 );

 
CREATE TABLE matches_table (
	unique_match_id 	SERIAL,
	winner_id	 			INTEGER REFERENCES player_table(unique_player_id),
	loser_id			 	INTEGER REFERENCES player_table(unique_player_id),	
	primary key (unique_match_id)
);

CREATE VIEW matches_count_view AS 
           (SELECT unique_player_id, player_name, 
               (SELECT COUNT(winner_id) 
		        FROM matches_table 
			    WHERE unique_player_id = winner_id) AS wins 
			FROM player_table 
			GROUP BY unique_player_id, player_name 
			ORDER BY wins DESC);


	
 
 
