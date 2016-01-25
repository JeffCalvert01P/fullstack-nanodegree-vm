#!/usr/bin/env python
# 
# tournament_dbsql.py -- SQL for implementation of a Swiss-system tournament
#


def deleteMatchesSQL():
    """Remove all the match records from the database.

    Returns:
      SQL sting to delete match records
    """
 
    return "DELETE FROM matches_table"


def deletePlayersSQL():
    """
    Remove all the player records from the database.

    Returns:
      SQL string to delete player records
    """

    return "DELETE FROM player_table"
 

def selectAllPlayersSQL():
    """
    Returns the players currently registered.

    Returns:
      SQL string to query all player records
    """
    
    return "SELECT * FROM player_table"


def registerPlayerSQL():
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.

    Returns:
      SQL string to insert player records
    """

    return "INSERT INTO player_table (player_name) VALUES(%s)"


def playerStandingsSQL():

    """Reurns a list of the players in order of their standings

    Returns:
      SQL string to insert player records

    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      SQL query string to get player standings
    """
    return "SELECT unique_player_id, player_name, \
                (SELECT COUNT(*) \
                 FROM matches_table \
                 WHERE unique_player_id = winner_id) AS winner, \
                (SELECT COUNT(*) \
                 FROM matches_table \
                 WHERE unique_player_id = winner_id OR \
                       unique_player_id = loser_id) AS matches \
            FROM player_table ORDER BY winner, matches"


def reportMatchInsertSQL():
    """Records the outcome of a single match between two players.

    Returns:
      SQL string to insert entry into matches table
    """

    return "INSERT INTO matches_table (winner_id, loser_id) VALUES(%s, %s)"

 
def returnPlayerOrderSQL():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      SQL stringto get the player order 
    """
    return "select unique_player_id, player_name from matches_count_view"
    
