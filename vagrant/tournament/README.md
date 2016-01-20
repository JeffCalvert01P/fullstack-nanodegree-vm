tournament.py
tournament_ec.py

There are 2 python modules included.  tournament.py address the basic project.  tournament_ec.py has all the extra credit features.

Both python modules use swiss pairing to match players for a tournament.

Instructions

This assumes that you have a vagrant environment and a postgesql environment established

1) Extract the following files into a common project directory under a tournament directory

Base project
	- tournament_test.py
	- tournament.py
	- tournament.sql
	
Extra credit project	
	- tournament_test_ec.py
	- tournament_ec.py
	- tournament_ec.sql

2) Establish the database for the project you will run.
- Navigate to the fullstack-nanodegree-vm directory
- "vagrant ssh" to the server
- navigate to the tournament directory
- navigate to the vagrant director cd /vagrant
- access the database server by entering psql 
- create the database by typing CREATE DATABASE tournament;
- set-up the database tables and views by loading the appropriate file \i tournament.sql or tournament_ec.sql
- Exit the database server by entering \q

3) Run the corresponding python modules
- Enter python tournament_test.py to run the basic module
- Enter python tournament_test_ec.py to run the extra credit module

4) The basic module will report that each test was successful
5) The extra credit module will report the number of players, the number of matches and list out the player standings at the end of each round