#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import tournament_dbsql


def connect():

    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(tournament_dbsql.deleteMatchesSQL())
    connection.commit()
    connection.close


def deletePlayers():
    """Remove all the player records from the database.

    Args:
      tournament: the tournament number
    """

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(tournament_dbsql.deletePlayersSQL())
    connection.commit()
    connection.close


def countPlayers():
    """Returns the number of players currently registered.

    Args:
      tournament: the tournament number
    """

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(tournament_dbsql.selectAllPlayersSQL())
    rows = cursor.rowcount
    connection.close
    return rows


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    data = (name, )
    cursor.execute(tournament_dbsql.registerPlayerSQL(), data)
    connection.commit()
    connection.close


def playerStandings():

    """Reurns a list of the players in order of their standings

    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    
    cursor.execute(tournament_dbsql.playerStandingsSQL())
    
    rows = cursor.fetchall()
    connection.close

    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # add to the wins and matches for the winner
    connection = connect()
    cursor = connection.cursor()
    data = (winner, loser)
    cursor.execute(tournament_dbsql.reportMatchInsertSQL(), data)
    connection.commit()
    connection.close

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection = connect()
    cursor = connection.cursor()

    """
    Return players in order of most winners so the winners get matched with
    the winners and the losers get matched with the losers.

    query = "select unique_player_id, player_name from matches_count_view"
    """
    
    cursor.execute(tournament_dbsql.returnPlayerOrderSQL())

    count = 0
    pairing = ()
    pairing_list = []

    for row in cursor:

        count += 1

        if count < 2:
            player1 = row
        else:
            pairing = player1 + row
            pairing_list.append(pairing)
            pairing = ()
            count = 0
            
    connection.close

    return pairing_list
