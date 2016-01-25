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
	tournament 		integer,
	unique_player_id 	SERIAL PRIMARY KEY,
	player_name 	VARCHAR(80)
 );
 
CREATE TABLE matches_table (
	unique_match_id 	SERIAL,
	tournament 	 		integer,
	winner_id 			INTEGER,
	loser_id 			INTEGER,
	round_num 			INTEGER,
	tie_ind 			VARCHAR(1),
 	primary key (tournament, winner_id, loser_id)
	);

-- Create view to show competitor match count
CREATE VIEW competitor_count_view 
AS (SELECT a.unique_player_id,
	(SELECT COUNT(winner_id) counts
	FROM matches_table c
	WHERE b.winner_id = c.winner_id
	GROUP BY c.winner_id
	ORDER BY counts DESC
	LIMIT 1) as comp_wins
	FROM player_table a, matches_table b 
	WHERE (b.winner_id = a.unique_player_id OR b.loser_id = a.unique_player_id)
	GROUP BY comp_wins, a.unique_player_id
	ORDER BY comp_wins DESC);
	
	
CREATE VIEW matches_count_view 
AS (SELECT pt.tournament, pt.unique_player_id, pt.player_name, 
	    (SELECT COUNT(mt.winner_id) 
         FROM matches_table mt 
         WHERE pt.unique_player_id = mt.winner_id) AS wins, 
        (SELECT COUNT(mt2.winner_id) 
         FROM matches_table mt2 
         WHERE ((pt.unique_player_id = mt2.winner_id or
		       pt.unique_player_id = mt2.loser_id) and
               mt2.tie_ind <> 'Y')) AS matches, 
        (SELECT comp_wins 
         FROM competitor_count_view cc
         WHERE pt.unique_player_id = cc.unique_player_id
		 LIMIT 1) AS comp_wins 
  	 FROM player_table pt
	 GROUP BY unique_player_id, player_name 
	 ORDER BY wins DESC, comp_wins DESC);

	
 
 
