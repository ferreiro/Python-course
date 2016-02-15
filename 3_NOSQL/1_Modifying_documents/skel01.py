# -*- coding: utf-8 -*-
"""
Authors: Jorge Ferreiro & Tommaso Innocenti
"""

dbName = 'giw';

from bottle import post, get, request, route, run, template, static_file
import pymongo
from pymongo import MongoClient # install MongoClient
from pymongo import ReturnDocument
import json

client 	= MongoClient()
db 		= client['giw']
users 	= db['users']

# Error or success messages as global variable

msg = {
	'insertion' : {
		'success' : 'User added to our database',
		'error' : {
			'duplicate'	:	'The username is already on our system',
			'invalid' 	: 	'Sorry. Zip or Year are not valid. They must be numbers.'
		}
	}
}


#####################################
########## ASSETS ROUTING ###########
#####################################

@route('/views/<filepath:path>')
def file_stac(filepath):
    return static_file(filepath, root="./views")

@route('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/')

@route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/')

@route('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/')

@route('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='static/')

# ¡MUY IMPORTANTE!
# Todas las inserciones se deben realizar en la colección 'users' dentro de la
# base de datos 'giw'.

####################################
########### GET METHODS ############
####################################

@get('/')
def index():
	return template('index');

@get('/change_email')
def change_email_view():
	return template('change_email');

@get('/insert')
def insert__view():
	return template('insert');

@get('/insert_or_update')
def insert_or_update_view():
	return template('insert_or_update');

@get('/delete')
def delete_view():
	return template('delete');

# Display user profile.
@get('/delete_year')
def delete_by_year_view():
	return template('delete_year');

# Display user profile.
@get('/<userID>')
def display_user_byID_view(userID):
	try:
		cursor = db.users.find({
			'_id' : userID
		});

		if (cursor.count() > 0): 
			user = cursor[0]
			return template('profile', user=user);
		
		return template('result', message="User doesn't exist...");
	except:
		return template('result', message="Problems retrieving that user");

@get('/<userID>/edit')
def edit_user_byID_view(userID):
	cursor = db.users.find({
		'_id' : userID
	});

	if (cursor.count() == 0):
		print "No user with that ID"
		return "No user with that ID"
	else:
		user = cursor[0] # python dictionary from a user
		return template('change_email_profile', user=user);

'''
	Aux:
	Return true if a given input don't contains
	only a digit. False if is a digit.
	We cast inputted value to use the isdigit()
	method on strings 
'''
def noDigit(integerValue):
	return not str(integerValue).isdigit() # cast to string

def isDigit(integerValue):
	return str(integerValue).isdigit() # cast to string

#####################################
########### POST METHODS ############
#####################################

''' 
	Insert a new user into our database
	Only if user doesn't exist on our system.
	When success, print a message and show
	a success view.
'''

@post('/add_user')
def add_user_post():

	zip		= request.forms.get('zip')
	year 	= request.forms.get('year')

	if not (isDigit(zip) and isDigit(year)):
		invalidTypeErr = msg['insertion']['error']['invalid']
		print 'Error: ' + invalidTypeErr
		return template('result', message=invalidTypeErr)

	try:
		# Try to add the user to our database
		cursor = users.insert_one({
			'_id' 		: str(request.forms.get('_id')),
			'address'	: {
				'country'	: str(request.forms.get('country')),
				'zip'		: int(zip)
			},
			'email'		: str(request.forms.get('email')),
			'gender'	: str(request.forms.get('gender')),
			'likes'		: str(request.forms.get('likes')).split(','), 
			'password'	: str(request.forms.get('password')),
			'year'		: int(year)
		});
	except pymongo.errors.DuplicateKeyError, e:
		print 'Error: ' + msg['insertion']['error']['duplicate'] + '\n'
		return template('result', message=msg['insertion']['error']['duplicate'])
	
	print 'Success: ' + msg['insertion']['success'] + '\n'
	return template('result', message=msg['insertion']['success'])

'''
	Update email of a user that already exists in the collection.
	Como resultado de esta petición el servidor web debe mostrar el número de documentos modificados.
'''
@post('/change_email')
def change_email():

	_id 	= str(request.forms.get('_id'))
	email 	= str(request.forms.get('email'))

	updatedUser = None; # User object | None= user doesn't exist

	try:
		updatedUser = users.find_one_and_update(
			{	
				'_id':_id 
			},
			{
				'$set' : {
					'email':email
				}
			},
			return_document=ReturnDocument.AFTER
		);

	except ValueError:
		print "Email coudln't change"
	
	if updatedUser != None:
		# The user exists. Show his profile
		print "\n 1 documents modified\n"
		return template('profile', user=updatedUser);
	
	print "\n 0 documents modified\n"
	return template('result', message="[ BAD ] Your user NOT exist on our database")


'''
	Try to insert a new user.
	If the user is already on our database,
	data will be updated.
'''
@post('/insert_or_update')
def insert_or_update():
    
    zip		= request.forms.get('zip')
    year 	= request.forms.get('year')

    if not (isDigit(zip) and isDigit(year)):
    	invalidTypeErr = msg['insertion']['error']['invalid']
    	print 'Error: ' + invalidTypeErr
    	return template('result', message=invalidTypeErr)

    try:
    	userID = str(request.forms.get('_id'));

    	doc = users.find_one_and_update(
    		{
    			'_id' :userID
    		},
    		{
    			'$set' : {
	    			'address' : {
		    			'country': str(request.forms.get('country')),
			    		'zip': int(zip)
	    			},
		    		'email': str(request.forms.get('email')),
		    		'gender': str(request.forms.get('gender')),
		    		'likes': str(request.forms.get('likes')).split(','), # Create array of strings.
		    		'password': str(request.forms.get('password')), 
		    		'year': int(year)
    			}
    		},
    		upsert=True,
    		return_document=ReturnDocument.BEFORE);

    	if doc == None:
    		message="\nThe user wasn't on our system. Inserting!\n"
    	else:
    		message="\nThe user was on the system. Modifying it!\n"
    		
    except ValueError:
    	message = ValueError;

    print message
    return template('result', message=message)

@post('/delete')
def delete_id():

	_id = str(request.forms.get('_id'));
	deleted = users.find_one_and_delete({'_id': _id});
	
	if deleted != None:
		print "\n1 document deleted from the system"
		return template('result', message="User deleted successfully!");
	
	print "\n0 document deleted from the system"
	return template('result', message="User doesn't exist!");

@post('/delete_year')
def delete_year():

	numDeleted = 0
	year = int(request.forms.get('year'))
	cursor = users.find({'year':year})

	for s in cursor:
		_id = s['_id'] 
		deleted = users.find_one_and_delete({'_id': _id});
		if deleted != None:
			numDeleted += 1

	msg = "deleted " + str(numDeleted) + " documents"
	print msg

	return template('result',message=msg)

@route('/*')
def error():
	return "Not found"

run(host='127.0.0.1', port=3000);

