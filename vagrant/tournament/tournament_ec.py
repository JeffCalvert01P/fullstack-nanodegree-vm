#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import tournament_dbsql_ec


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(tournament_dbsql_ec.deleteMatchesSQL())
    connection.commit()
    connection.close


def deletePlayers():
    """Remove all the player records from the database.
    """

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(tournament_dbsql_ec.deletePlayersSQL())
    connection.commit()
    connection.close


def countPlayers(tournament):
    """Returns the number of players currently registered.

    Args:
      tournament: the tournament number
    """

    connection = connect()
    cursor = connection.cursor()
    data = (tournament,)
    cursor.execute(tournament_dbsql_ec.selectAllPlayersSQL(), data)
    row_count = cursor.rowcount
    connection.close
    return row_count


def registerPlayer(tournament, name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    data = (tournament, name)
    cursor.execute(tournament_dbsql_ec.registerPlayerSQL(), data)
    connection.commit()
    connection.close


def playerStandings(tournament):

    """Reurns a list of the players in order of their standings

    Args:
      tournament: the tournament number

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

    #    Query player standings
    cursor.execute(tournament_dbsql_ec.playerStandingsSQL(), (tournament,))
    
    rows = cursor.fetchall()

    connection.close

    return rows


def reportMatch(tournament, winner, loser, round_num, tie_ind):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the tournament number
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      round_num: the current round of matches
      tie_ind: indicates whether the match was a tie
    """

    """
    I always put the lesser player id in the player 1 id to limit the
    number of rows and keep the data cleaner
    """
    if winner > loser:
        player1 = loser
        player2 = winner
    else:
        player2 = loser
        player1 = winner

    # Insert record for matches table
    connection = connect()
    cursor = connection.cursor()
    data = (tournament, player1, player2, round_num, tie_ind)
    cursor.execute(tournament_dbsql_ec.reportMatchInsertSQL(), data)

    """
    Insert a record in the matches table when there is a tie
    to give the second player credit
    """
    
    if tie_ind == "Y":
        data = (tournament, player2, player1, round_num, tie_ind)
        cursor.execute(tournament_dbsql_ec.reportMatchInsertSQL(), data)
         
    connection.commit()
    connection.close

 
def swissPairings(tournament, round_num):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Args:
      tournament: the tournament number
      round_num: the current round of matches

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(tournament_dbsql_ec.playerOrderSQL(), (tournament,))

    count = 0
    row_count = 0
    pairing = ()
    pairing_list = []

    matchq_connection = connect()
    match_connection = connect()

    for row in cursor:
        count += 1
        row_count += 1

        if count < 2:
            # Hold the first of each pair for later matching
            player1 = row
        else:
            # Make sure the smaller value is in first position
            if player1[0] < row[0]:
                player1_id_h = player1
                player2_id_h = row
            else:
                player2_id_h = player1
                player1_id_h = row
                
    # check for duplicates - Extra Credit 1 - I also put
    # constraints on the database.

            matchq_cursor = connection.cursor()
            data = (tournament, player1_id_h[0], player2_id_h[0])
            matchq_cursor.execute(tournament_dbsql_ec.checkMatchExistsSQL(), data)
            matchq_connection.commit()
            count = 0;
    # if no match found, pair the players
            if matchq_cursor.rowcount == 0:
                pairing = player1_id_h + player2_id_h
                pairing_list.append(pairing)
                pairing = ()
 
    # Insert the matched players into the match table

    matchq_connection.close
    connection.close

    """
    Append last player with a dummy negative record so they get credit for a win,
    but do not appear in a match. I removed the table contraint to allow for -1
    """

    if (round_num == 0 and cursor.rowcount % 2 > 0 and
            row_count == cursor.rowcount):
        pairing = player1 + (-1, ' ')
        pairing_list.append(pairing)
        # print pairing_list

    return pairing_list
