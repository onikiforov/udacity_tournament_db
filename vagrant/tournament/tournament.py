#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import bleach
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute('DELETE FROM matches')
    c.execute('ALTER SEQUENCE matches_id_seq RESTART WITH 1')
    c.execute('UPDATE players SET wins = 0')
    c.execute('UPDATE players SET matches = 0')
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    deleteMatches()  # We should delete matches before deleting players, because of KEY relations
    c.execute('DELETE FROM players')
    c.execute('ALTER SEQUENCE players_id_seq RESTART WITH 1')
    # c.execute('TRUNCATE players RESTART IDENTITY CASCADE') # Possible alternative in one command
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM players')
    count = c.fetchone()[0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute('INSERT INTO players (name) VALUES (%s)', (bleach.clean(name),))
    conn.commit()
    conn.close()


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
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT * FROM players ORDER BY wins DESC')
    player_standings = c.fetchall()
    conn.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute('INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)', (winner, loser))
    c.execute('UPDATE players SET wins = wins + 1 WHERE id = %s', (bleach.clean(str(winner)),))
    c.execute('UPDATE players SET matches = matches + 1 WHERE id in (%s, %s)', (winner, loser))
    conn.commit()
    conn.close()
 
 
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
    players = playerStandings()
    pairs_list = []
    for i in range(0, len(players)-1, 2):
        pair = (players[i][0], players[i][1], players[i+1][0], players[i+1][1])
        pairs_list.append(pair)
    return pairs_list
