rdb-fullstack
=============

Submission for project 2 of the Full Stack Web Dev nanodegree.

About
=====

Python file to manipulate a PostgreSQL DB, along with an attached test suite.

The steps below detail connection, bootstrapping and running steps:

* `$ vagrant up && vagrant ssh`
* `$ psql`
* `=> CREATE DATABASE tournament;`
* `=> \c tournament`
* `=> \i tournament.sql`
* `=> \q`
* `$ python tournament_test.py`
