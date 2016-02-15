#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Authors: Jorge Ferreiro & Tommaso Innocenti
""" 

from bottle import run, post, get
import hashlib
import pymongo
import onetimepass as otp
import random
import string
from passlib.hash import pbkdf2_sha256
from bottle import request, route, run, template, response, static_file
from pymongo import MongoClient

client  = MongoClient()
db      = client['giw']

APP_NAME = "sudoNotes"

"""
User Schema

	User = {
		"_id" : username,
		"name": name,
		"country" : country,
		"email": email,
		"password" : password
	} 

"""


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

#################################
########## ENCRYPTION ###########
########## SECURITY   ###########
#################################

def encryptPass(password):
	rounds = random.randint(35000,60000) # random rounds
	salt_size = random.randint(800,900) # random salt size
	return pbkdf2_sha256.encrypt(password, rounds=rounds, salt_size=salt_size)

def validPassword(password, hash):
	try:
		return pbkdf2_sha256.verify(password, hash);
	except: # The password is not well formated (eg, using pbkd2_sha256 algorithm)
 		return False

# Redirecting to login when acessing home
@get('/')
def home():
	response.status = 303
	response.set_header('Location', '/login')

##############
# APARTADO A #
##############

@get('/signup')
def signup_view():
	return template('signup_login', signup=True);

@post('/signup')
def signup():

	username    = str(request.forms.get('username')).lower() # Store in lowercase
	name        = str(request.forms.get('name')).lower()
	country     = str(request.forms.get('country')).lower()
	email       = str(request.forms.get('email')).lower()
	password    = str(request.forms.get('password')).lower()
	password2   = str(request.forms.get('password2')).lower()  

	if password != password2:
		return template('result', message="Password doesn't match");

	result = db.users.find({ "_id": username })

	if result.count() > 0:
		return template('result', message="Username is already registered on our database");
 
	encryptedPassword = encryptPass(password);

	User = {
		"_id"       : username,
		"name"      : name,
		"country"   : country,
		"email"     : email,
		"secretKey" : None, # used in the second part of the assigmnet
		"password"  : encryptedPassword
	}

	db.users.insert_one(User); # Valid user to this point. Insert it on the database.+
	return template('welcome', user=User);
 
@get('/change_password')
def signup_view():
	return template('change_password');

@post('/change_password')
def change_password():
	
	username    = str(request.forms.get('username')).lower() # Store string in lowercase
	oldPassword = str(request.forms.get('oldpassword')).lower()
	newPassword = str(request.forms.get('newpassword')).lower()

	user = db.users.find_one({ 
		"_id" : username 
	});

	if not user: # Username doesn't exists
		return template('result', message='Usuario o contraseña incorrectos');
 
	if not validPassword(oldPassword, user['password']): # Old password doesnt match
		return template('result', message='Usuario o contraseña incorrectos');

	newPasswordEncrypted = encryptPass(newPassword);
	db.users.update_one(
		{ "_id" : username }, 
		{ "$set": { "password" : newPasswordEncrypted }
	});
	return template('result', message='Congratulations!! Password modified!!');

@get('/login')
def login_view(): 
	return template('signup_login', signup=False);

@post('/login')
def login():
	
	username = str(request.forms.get('username')).lower() # Store string in lowercase
	password = str(request.forms.get('password')).lower()

	User = db.users.find_one({ 
		"_id" : username 
	});

	if not User: # Username doesn't exists
		return template('result', message='Usuario o contraseña incorrectos');
 
	if not validPassword(password, User['password']): # Old password doesnt match
		return template('result', message='Usuario o contraseña incorrectos');

	# For security reasons, remove secret Key and password 
	# from the User Dictionary before return them to the view.
	del User['secretKey'] 
	del User['password']

	return template('welcome', user=User);

##############
# APARTADO B #
##############

def gen_secret():
	# Genera una cadena aleatoria de 16 caracteres a escoger entre las 26 
	# letras mayúsculas del inglés y los dígitos 2, 3, 4, 5, 6 y 7. 
	#
	# Ejemplo:
	# >>> gen_secret()
	# '7ZVVBSKR22ATNU26'
	length = 16
	chars = string.ascii_uppercase + "234567"
	return ''.join(random.choice(chars) for x in range(length))
	
def gen_gauth_url(app_name, username, secret):
	# Genera la URL para insertar una cuenta en Google Authenticator
	#
	# Ejemplo:
	# >>> gen_gauth_url( 'GIW_grupoX', 'pepe_lopez', 'JBSWY3DPEHPK3PXP')
	# 'otpauth://totp/pepe_lopez?secret=JBSWY3DPEHPK3PXP&issuer=GIW_grupoX
	#    
	# Formato de la URL:
	# otpauth://totp/<ETIQUETA>?secret=<SECRETO>&issuer=<NOMBRE_APLICACION_WEB>
	#
	# Más información en: 
	#   https://github.com/google/google-authenticator/wiki/Key-Uri-Format
	app_name = str(app_name).lower()
	username = str(username).lower()
	secret   = str(secret).lower()
	gauth_url = "otpauth://totp/%s?secret=%s&issuer=%s" % (username, secret, app_name)
	return gauth_url;

def gen_qrcode_url(gauth_url):
	# Genera la URL para generar el código QR que representa 'gauth_url'
	# Información de la API: http://goqr.me/api/doc/create-qr-code/
	#
	# Ejemplo:
	# >>> gen_qrcode_url('otpauth://totp/pepe_lopez?secret=JBSWY3DPEHPK3PXP&issuer=GIW_grupoX')
	# 'http://api.qrserver.com/v1/create-qr-code/?data=otpauth%3A%2F%2Ftotp%2Fpepe_lopez%3Fsecret%3DJBSWY3DPEHPK3PXP%26issuer%3DGIW_grupoX'
	base = "http://api.qrserver.com/v1/create-qr-code/?data="
	return base + str(gauth_url)
	
@get('/signup_totp')
def login_view(): 
	return template('signup_login_totp', signup=True);

@post('/signup_totp')
def signup_totp():
	global APP_NAME # using when exporting the QR!!!

	username    = str(request.forms.get('username')).lower() # Store in lowercase
	name        = str(request.forms.get('name')).lower()
	country     = str(request.forms.get('country')).lower()
	email       = str(request.forms.get('email')).lower()
	password    = str(request.forms.get('password')).lower()
	password2   = str(request.forms.get('password2')).lower()  

	if password != password2:
		return template('result', message="Password doesn't match");

	result = db.users.find({ "_id": username })

	if result.count() > 0:
		return template('result', message="Username is already registered on our database");
	
	secretKey = gen_secret(); # Generate a 16 bits random private key (for google autenticator)
	encryptedPassword = encryptPass(password);

	User = {
		"_id"       : username.lower(),
		"name"      : name,
		"country"   : country,
		"email"     : email,
		"secretKey" : secretKey,
		"password"  : encryptedPassword
	}

	insertedUser = db.users.insert_one(User); # Valid user to this point. Insert it on the database.+

	# Generate QR image to return the user
	gauth_url   = gen_gauth_url(APP_NAME, User['_id'], User['secretKey']);
	qrcode      = gen_qrcode_url(gauth_url)

	return template('welcome_secondFactor', user=User, qrcode=qrcode);
	  
@get('/login_totp')
def login_view(): 
	return template('signup_login_totp', signup=False);
  
@post('/login_totp')        
def login_totp():
	
	username = str(request.forms.get('username')).lower()
	password = str(request.forms.get('password')).lower()
	totpCode = str(request.forms.get('totpCode')).lower()
 
	User = db.users.find_one({ 
		"_id" : username 
	});
 
	if not User: # Username doesn't exists
		return template('result', message='Usuario o contraseña incorrectos');
	
	if not validPassword(password, User['password']): # Old password doesnt match
		return template('result', message='Usuario o contraseña incorrectos');
  
	token = totpCode
	secret = User['secretKey']
	valid = otp.valid_totp(token, secret)

	if not valid:
		return template('result', message='Usuario o contraseña incorrectos')
	
	# For security reasons, remove secret Key and password 
	# from the User Dictionary before return them to the view.
	del User['secretKey'] 
	del User['password']

	return template('welcome', user=User);
	
if __name__ == "__main__":
	run(host='localhost',port=8080,debug=True)

###############################################################################
################# Funciones auxiliares a partir de este punto #################
###############################################################################

