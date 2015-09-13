#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

DATABASE = 'tournament'


def connect():
    """
    Connect to the PostgreSQL database.  Returns a database connection.
    """
    return psycopg2.connect("dbname={0}".format(DATABASE))


def get_db_and_cursor():
    """
    Helper function to return a db object and a cursor.
    """
    db = connect()
    cursor = db.cursor()
    return db, cursor


def query_exec(query):
    """
    Helper function to perform queries that don't take params
    Args:
      query: The SQL query to execute
    """
    db, cursor = get_db_and_cursor()
    cursor.execute(query)
    db.commit()
    db.close()
    return True


def deleteMatches():
    """
    Remove all the match records from the database.
    """
    query = 'DELETE FROM match'
    query_exec(query)


def deletePlayers():
    """
    Remove all the player records from the database.
    """
    query = 'DELETE FROM player'
    query_exec(query)


def countPlayers():
    """
    Returns the number of players currently registered.
    """
    query = 'SELECT COUNt(id) FROM player'
    db, cursor = get_db_and_cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return int(result[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    query = 'INSERT INTO player (name) VALUES (%s)'
    db, cursor = get_db_and_cursor()
    cursor.execute(query, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    query = '''
        SELECT wins.id, wins.name, wins, (wins + losses) AS total
        FROM wins LEFT JOIN losses
        ON wins.id = losses.id'''

    db, cursor = get_db_and_cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    query = 'INSERT INTO match (winner, loser) VALUES \
             (%s, %s)'
    db, cursor = get_db_and_cursor()
    cursor.execute(query, (winner, loser,))
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
    players = [player for player in playerStandings()]
    if len(players) < 2:
        raise ValueError('Tournament needs at least one pair')
    player_one = []
    player_two = []
    # The following loop takes adjacent players and puts them in lists
    for i, player in enumerate(players):
        if i % 2 == 0:
            player_one.append(player)
        else:
            player_two.append(player)

    # A pair is just adjacent players, so we can simply zip up the lists
    pairs = zip(player_one, player_two)
    results = []
    # Inefficient, since we are creating a temporary list
    for pair in pairs:
        results.append((pair[0][0], pair[0][1], pair[1][0], pair[1][1]))

    return results
