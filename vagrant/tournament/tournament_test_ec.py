#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament_ec import *


def runSwissSystem():

    ## added tournament number throughout to support mutiple tournaments
    tournament = 1
    ## comment the following to 2 lines to run with multiple tournaments
    deleteMatches()
    deletePlayers()

    registerPlayer(tournament, "Twilight Sparkle")
    registerPlayer(tournament, "Fluttershy")
    registerPlayer(tournament, "Applejack")
    registerPlayer(tournament, "Pinkie Pie")
    registerPlayer(tournament, "Applejack   xxxxx")
    registerPlayer(tournament, "Pinkie Pie   zzzzz")
    registerPlayer(tournament, "Applejack   xxxxx")
    registerPlayer(tournament, "Pinkie Pie   zzzzz 2")
    registerPlayer(tournament, "Pinkie Pie   zzzzz 3")

    c = countPlayers(tournament)
    print("The following number of players are register:", c)
    
    ## Mr. Model formula http://senseis.xmp.net/?SwissPairing - Number of players + (7 * places) /5.

    r = ((c + (7 * 1)) /5)

    print("There will the following number of rounds: ", r)

    # Do initial pairings
    # pairings = swissPairings(tournament)

    ## tie_ind is used to introduce tie matches occassionally
    tie_ind = "N"

    ## Loop through for each round
    for i in range (0, r):
        pairings = swissPairings(tournament, i)
        tie_ind = "Y"

    ## Loop through the pairing Tuples
        for row in pairings:
            reportMatch(tournament, row[0], row[2], i, tie_ind)
            tie_ind = "N"

    ## print standing at end of each round
        standings = playerStandings(tournament)
        print "round: ", i, "standings: ", standings;

    
    print "Swiss pairings complete."


if __name__ == '__main__':
    runSwissSystem()

