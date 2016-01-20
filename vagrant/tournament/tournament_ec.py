#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from matches_table")
    connection.commit()
    connection.close

def deletePlayers():
    """Remove all the player records from the database.

    """

    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from player_table")
    connection.commit()
    connection.close


def countPlayers(tournament):
    """Returns the number of players currently registered.

    Args:
      tournament: the tournament number
    """

    connection = connect()
    cursor = connection.cursor()
    query = "SELECT * FROM player_table where tournament = %s"
    data = (tournament,)
    cursor.execute(query, data)
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
    query = "INSERT INTO player_table (tournament, player_name, wins, matches) values(%s, %s, %s, %s)"
    data = (tournament, name, 0, 0)
    cursor.execute(query, data)
    connection.commit()
    connection.close

 

def playerStandings(tournament):

    """Reurns a list of the players in order of their standings

    Args:
      tournament: the tournament number

    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()

    """
        Do a left join with the player_table and matches view to get the wins from the player table and the competitors wins from the matches count view.  Left join is required because matches view will not have a row
        for a player that never lost.  Order desc on wins and counts so I can get the player with the most wins.  If there is a tie, then the count will give me the player with the competitors with the most wins
    """
    
    query = "select a.unique_player_id, player_name, wins, matches from player_table a left join matches_count_view b on a.unique_player_id = b.unique_player_id and tournament = %s order by wins desc, count desc;"
    cursor.execute(query,(tournament,))
    
    rows = cursor.fetchall()
    connection.close

    return rows;    


def reportMatch(tournament, winner, loser, round_num, tie_ind):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the tournament number
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      round_num: the current round of matches
      tie_ind: indicates whether the match was a tie
    """
    

    ## Update the matches, wins and result for the winner.  
    connection = connect()
    cursor = connection.cursor()
    query = "UPDATE player_table set wins = wins + %s, matches = matches + %s, last_result = %s where unique_player_id = %s and tournament = %s;"
    data = (1, 1, "W", winner, tournament)
    cursor.execute(query, data)
    connection.commit()

    ## Makes sure both teams receive credit for a win if there is a tie
    if tie_ind == "Y":
        winner_value = 1
    else:
        winner_value = 0
 
    ## Update the matches, wins and result for the loser or tie.  
    query = "UPDATE player_table set wins = wins + %s,matches = matches + %s, last_result = %s where unique_player_id = %s and tournament = %s;"
    data = (winner_value, 1, "L", loser, tournament)
    cursor.execute(query, data)
    connection.commit()

    ## I always put the lesser player id in the player 1 id to limit the number of rows and keep the data cleaner
    if winner > loser:
        player1 = loser
        player2 = winner
    else:
        player2 = loser
        player1 = winner

    ## Update the matches table with the results 
    connection = connect()
    cursor = connection.cursor()
    query = "UPDATE matches_table set round_num = %s, winner_id = %s, tie_ind = %s where tournament = %s and player1_id = %s and player2_id = %s;"
    data = (round_num, winner, tie_ind, tournament, player1, player2)
    cursor.execute(query, data)

    ## Insert a record in the matches table when there is a tie to give the second player credit 
    if tie_ind == "Y":
        query = "INSERT INTO matches_table (tournament,player1_id, player2_id, winner_id, round_num,tie_ind) values(%s, %s, %s, %s, %s, %s)"
        data = (tournament, player2, player1, loser, round_num, tie_ind)
        cursor.execute(query, data)
         
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
    
    query = "SELECT unique_player_id, player_name FROM player_table where tournament = %s order by matches, wins desc, last_result desc;"
    data = (tournament)
    
    cursor.execute(query, (tournament,))

    count = 0
    row_count = 0
    pairing = ()
    pairing_list = []

    matchq_connection = connect()
    match_connection = connect()
    
    for row in cursor:

        count += 1
        row_count +=1

        if count < 2:
        ## Hold the first of each pair for later matching
            player1 = row
        else:
            ## Make sure the smaller value is in first position
            if player1[0] < row[0]:
                player1_id_h = player1
                player2_id_h = row
            else:
                player2_id_h = player1
                player1_id_h = row
                
    ## check for duplicates - Extra Credit 1 - I also put constraints on the database.
            matchq_cursor = connection.cursor()
            query = "SELECT * FROM matches_table WHERE tournament = %s and player1_id = %s and player2_id = %s"
            data = (tournament, player1_id_h[0], player2_id_h[0])
            matchq_cursor.execute(query, data)
            matchq_connection.commit()
  
    ## if no match found, pair the players
            if matchq_cursor.rowcount == 0:
                pairing = player1_id_h + player2_id_h
                pairing_list.append(pairing)
                pairing = ()
 
    ## Insert the matched players into the match table

                match_cursor = match_connection.cursor()
                query = "INSERT INTO matches_table (tournament,player1_id, player2_id, round_num) values(%s, %s, %s, %s)"
                data = (tournament, player1_id_h[0], player2_id_h[0], round_num)
                match_cursor.execute(query, data)
                match_connection.commit()
                count = 0            

    matchq_connection.close
    match_connection.close
    connection.close

    ## append last player with a dummy negative record so they get credit for a win, but do not appear in a match
    if (round_num == 0 and cursor.rowcount % 2 > 0 and row_count == cursor.rowcount):
        pairing = player1 + (-1, ' ')
        pairing_list.append(pairing)

    return pairing_list;    


