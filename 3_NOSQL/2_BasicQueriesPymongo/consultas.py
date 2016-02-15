# -*- coding: utf-8 -*-
"""
	Authors: Jorge Ferreiro & Tommaso Innocenti

	IMPLICIT SCHEME

	+---------------------------------------------------+
	| key             | types  | occurrences | percents |
	| --------------- | ------ | ----------- | -------- |
	| _id             | String |        1000 |    100.0 |
	| address         | Object |        1000 |    100.0 |
	| address.country | String |        1000 |    100.0 |
	| address.zip     | Number |        1000 |    100.0 |
	| email           | String |        1000 |    100.0 |
	| gender          | String |        1000 |    100.0 |
	| likes           | Array  |        1000 |    100.0 |
	| password        | String |        1000 |    100.0 |
	| year            | Number |        1000 |    100.0 |
	+---------------------------------------------------+

"""

from bottle import get, run, request, template

# Resto de importaciones
import pymongo
from pymongo import MongoClient # install MongoClient
from pymongo import ReturnDocument

client 	= MongoClient()
db 		= client['giw']


# http://localhost:8080/find_user_id?_id=user_1
@get('/find_user_id')
def find_user_id():
	
	maxParams   = 1 
	params  	= dict((k,request.query.getall(k)) for k in request.query.keys())
	validParams = ['_id']
	allRequired = True

	(valid, msg)= checkParameters(params, maxParams, validParams, allRequired) # Check if URL_ parameters are correct. Returning true/false and a message

	if valid:

		userID = params['_id'][0]
		cursor = db.users.find({'_id' : userID});
		
		userList   = [] 
		numResults = cursor.count()

		if numResults > 0:
			for user in cursor:
				userList.append(user) # We found some users. Compose a list of users

		return template('table', userList=userList, totalResults=numResults);

	else:
		return template('error', msg=msg)

# http://localhost:8080/find_users?gender=Male
# http://localhost:8080/find_users?gender=Male&year=2009
@get('/find_users')
def find_users():
	filter_and = True; # make and with all parameters
	return filterUsers_and_or(filter_and);

# http://localhost:8080/find_users_or?gender=Male&year=2000
@get('/find_users_or')
def find_users_or():
	filter_and = False; # make and with all parameters
	return filterUsers_and_or(filter_and);

# http://localhost:8080/find_like?like=football
@get('/find_like')
def find_like():
	
	maxParams   = 1 
	params      = dict((k,request.query.getall(k)) for k in request.query.keys())
	validParams = ['like']
	allRequired = True

	(valid, msg) = checkParameters(params, maxParams, validParams, allRequired)

	if valid:

		like = params['like']
		cursor = db.users.find({ 'likes': { '$in' : like }} );
		
		userList   = [] 
		numResults = cursor.count()

		if numResults > 0:
			# We found some users. Compose a list of users
			for user in cursor:
				userList.append(user)

		return template('table', userList=userList, totalResults=numResults);

	else:
		return template('error', msg=msg)

# http://localhost:8080/find_country?country=Spain
@get('/find_country')
def find_country():
	
	maxParams   = 1 
	params      = dict((k,request.query.getall(k)) for k in request.query.keys())
	validParams = ['country']
	allRequired = True

	(valid, msg)= checkParameters(params, maxParams, validParams, allRequired)

	if valid:
		
		country = params['country'][0]
		cursor = db.users.find({'address.country' : country});

		userList   = [] 
		numResults = cursor.count()

		# We found some users. Compose a list of users
		if numResults > 0:
			for user in cursor:
				userList.append(user)

		return template('table', userList=userList, totalResults=numResults);

	else:
		return template('error', msg=msg)

# http://localhost:8080/find_email_year?year=1992
@get('/find_email_year')
def email_year():
		
	maxParams   = 1 
	params      = dict((k,request.query.getall(k)) for k in request.query.keys())
	validParams = ['year']
	allRequired = True

	(valid, msg)= checkParameters(params, maxParams, validParams, allRequired)

	if valid:
		
		year = int(params['year'][0])
		cursor = db.users.find({'year' : year});

		userList   = []
		numResults = cursor.count()

		if numResults > 0:
			for user in cursor:
				userList.append(user)

		return template('table_special', userList=userList, totalResults=numResults);

	else:
		return template('error', msg=msg)


# http://localhost:8080/find_country_limit_sorted?country=Spain&limit=20&ord=asc
@get('/find_country_limit_sorted')
def find_country_limit_sorted():
	
	maxParams   = 3
	params      = dict((k,request.query.getall(k)) for k in request.query.keys())
	validParams = ['country', 'limit', 'ord']
	allRequired = True

	(isValid, msg) = checkParameters(params, maxParams, validParams, allRequired)

	if isValid:
		
		country = params['country'][0]
		limit = int(params['limit'][0])
		ord = str(params['ord'][0]).lower() # ord | desc
		
		if ord == 'asc':
			cursor = db.users.find({ 'address.country': country }).limit(limit).sort(
				[
					['year', pymongo.ASCENDING]
				]
			)
		elif ord == 'desc':
			cursor = db.users.find({ 'address.country': country }).limit(limit).sort(
				[
					['year', pymongo.DESCENDING]
				]
			)
		else:
			return template('error', msg="Sorry!! We can not order by this parameter")
		
		userList   = []
		numResults = cursor.count()

		if numResults > 0:
			for user in cursor:
				userList.append(user)
			
			if limit != 0 and numResults > limit:
				numResults = limit # return the number of limits results

		return template('table', userList=userList, totalResults=numResults);

	else:
		return template('error', msg=msg)


###############################################################################
################# Funciones auxiliares a partir de este punto #################
###############################################################################

''' 
	Returns a tuple where first index is a boolean value (Valid or False) 
	and the second parameter is an string with the error or success message
	
	Accepted parameters:
	1. Params: Dictionary where key is the name of param and value is an array of elements for this parameter
	2. MaxParams: Integer of maximun different keys (parameters name) it accepts.
	3. ValidParams: Dictionary of valid parameters accepted: validParams = { 'name', 'surname' }
'''		
def checkParameters(params, maxParams, validParams, allRequired):
	
	# Error type checking | source: http://stackoverflow.com/questions/2225038/determine-the-type-of-an-object
	if type(params) is not dict:
		return (False, 'Parameters are not dictionary type');
	elif type(maxParams) is not int:
		return (False, 'Maxium Parameters is not Integer Type');
	elif type(validParams) is not list:
		return (False, 'Valid Parameters are not List Type');

	# Now checks if the passed number of parameters are accepted.
	if len(params) == 0:
		return (False,'Empty Parameters. We only find when some parameters are provided')
	elif allRequired and len(params) < maxParams:
		return (False,'You don\'t provide all the parameters we need')
	elif len(params) > maxParams:
		return (False,'We don\'t accept more than ' + str(maxParams) + ' params passed by url')

	for key in params:
		
		totalParams = len(params[key]) # params associated with that key
		#print totalParams

		if totalParams > 1:
			errMsg = str(key) + " has " + str(totalParams) + " different values passing by params"; 
			return (False, errMsg)
		elif not key in validParams:
			errMsg = str(key) + " param is not valid" 
			return (False, errMsg);
		else:
			continue # The key params is valid

	return (True, 'Params are correct')



''' 
	Compose a query: returns array of Dictionaries
	where each element is each of the parameters we want to ask
	Structure: query = [ {"_id":_id},{"name":name}, ] 
'''

def composeQuery(params):

	query = [] # List of dictionaries (json objects)

	for key in params:
		elem  = {}
		value = params[key][0] # Params can have multiple values for each array element

		if key == 'year':
			value = int(value) # Cast to integer when year.

		elem[key] = value  # save value as dictionary
		query.append(elem) # push dictionary to query

	return query

''' 
This method can be used for find_users_or or find_users
the only that changes is that when you pass filter_and as true
the program will make an and of all the paramters 
and when or, it make an or on the query
'''

def filterUsers_and_or(make_and):

	params 		= dict((k,request.query.getall(k)) for k in request.query.keys())
	maxParams 	= 4
	validParams = ['_id', 'email', 'gender', 'year']
	allRequired = False # we accept less than maxParams as valid URL

	(valid, msg)= checkParameters(params, maxParams, validParams, allRequired) # Check if URL_ parameters are correct. Returning true/false and a message

	if valid:

		query  = composeQuery(params)

		if make_and:
			cursor = db.users.find({"$and":query});
		else:
			cursor = db.users.find({"$or":query});

		userList   = [] 
		numResults = cursor.count()

		if numResults > 0:
			# We found some users. Compose a list of users
			for user in cursor:
				userList.append(user)

		return template('table', userList=userList, totalResults=numResults);

	else:
		return template('error', msg=msg)



###############################################################################
###############################################################################

if __name__ == "__main__":
	run(host='localhost',port=8080,debug=True)
