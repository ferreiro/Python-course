
### How to import users to mongodb

1. open a shell (or a cmd console on windows).
	- Create a folder name "database" 
		$ mkdir database
	- Starting mongo server on that folder.
		$ mongod --dbpath database/
2. Open a new shell (or cmd).
	- Now we should import our model of users into database. Using mongoimport. Type:
	$ mongoimport --db giw --collection users users.json
