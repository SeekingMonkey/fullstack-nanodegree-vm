#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print "I am unable to connect to the database"


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM tournaments")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM tournaments")
    c.execute("DELETE FROM players")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
    data = c.fetchall()
    db.close()
    #print "data= ",data[0][0]
    count = data[0][0]
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players(PlayerName) VALUES (%s)", (name,))
    db.commit()
    c.execute("""INSERT INTO tournaments
              VALUES (default, (SELECT playerid FROM players WHERE playername = %s), 0, 0, 0, 0)""", (name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("""SELECT players.playerid, playername, wins, matches
              FROM players left join tournaments
              on players.playerid = tournaments.playerid""")
    dbData = c.fetchall()
    #print "dbData= ", dbData
    #print [{'matches': row[3], 'wins': row[2], 'name': str(row[1]), 'id': row[0]} for row in dbData]
    #print [{'id': row[0], 'name': str(row[1]), 'wins': row[2], 'matches': row[3]} for row in dbData]
    #print [(row[0], str(row[1]), row[2], row[3]) for row in dbData]
    players = [{'matches': row[3], 'wins': row[2], 'name': str(row[1]), 'id': row[0]} for row in dbData]
    db.close()
    return dbData

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    #print "winner: ",winner,"loser: ", loser
    db = connect()
    c = db.cursor()
    c.execute("""UPDATE tournaments
                SET wins=wins+1, matches=matches+1
                WHERE playerid = %s""", (winner,))
    c.execute("""UPDATE tournaments
                SET losses=losses+1, matches=matches+1
                WHERE playerid = %s""", (loser,))   
    db.commit()
    db.close()
 
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


