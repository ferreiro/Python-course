#!/usr/bin/env python
""" 
Authors: Jorge Ferreiro & Tommaso Innocenti
"""
# -*- coding: utf-8 -*-
from bottle import run, post, get, template,request, route, static_file, response
from time import gmtime, strftime
import time
import string
import random
import json
import urllib2
import urllib

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

# Credenciales. 
# https://developers.google.com/identity/protocols/OpenIDConnect#appsetup
# Copiar los valores adecuados.
config = {
    'client_id': '700570345546-cgc40e1j5rqgjj1asm08vjgap7sl5c5n.apps.googleusercontent.com',
    'client_secret': 'UJ1SiIYSi2pgcbrXAOQOgqL6',
    'response_type' : 'code',
    'redirect_uri' : 'http://localhost:8080/token',
    'scope' : 'email',
    'state' : 'XXX',
    'discovery_doc': 'https://accounts.google.com/.well-known/openid-configuration'
}

def gen_secret():
    # Genera una cadena aleatoria de 16 caracteres a escoger entre las 26 
    # letras mayúsculas del inglés y los dígitos 2, 3, 4, 5, 6 y 7. 
    #
    # Ejemplo:
    # >>> gen_secret()
    # '7ZVVBSKR22ATNU26'
    length = 30
    chars = string.ascii_uppercase + "234567"
    return ''.join(random.choice(chars) for x in range(length))

config['state'] = gen_secret();

@get('/login_google')
def login_google():
    global config
 
    url = "https://accounts.google.com/o/oauth2/v2/auth?"
    url += "client_id="      + config['client_id']
    url += "&response_type=" + config['response_type']
    url += "&redirect_uri="  + config['redirect_uri']
    url += "&scope="         + config['scope']
    url += "&state="         + config['state']

    return template('home', googleURL=url);

def getTokenEndPoint():
    global config
    data = json.load(urllib2.urlopen(config['discovery_doc']))
    return data['token_endpoint']

def getTokenJWKS_uri():
    global config
    data = json.load(urllib2.urlopen(config['discovery_doc']))
    return data['jwks_uri']

def getEncryptedToken(token_endpoint, userCode):
    global config 
   
    values = {
        'code' : userCode,
        'client_id' : config['client_id'],
        'client_secret' : config['client_secret'],
        'redirect_uri' : config['redirect_uri'],
        'grant_type' : 'authorization_code',
    }

    data = urllib.urlencode(values)
    req = urllib2.Request(token_endpoint, data)
    response = urllib2.urlopen(req)
    tokenDictionary = json.load(response) 
    return tokenDictionary

def getTokenData(id_token):
    url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?'
    url += 'id_token=' + id_token
    data = json.load(urllib2.urlopen(url))
    return data

def validateToken(tokenData):
    global config

    if tokenData['iss'] != 'https://accounts.google.com' and tokenData['iss'] != 'accounts.google.com':
        return False # tokenData is not from google
    if tokenData['aud'] != config['client_id']:
        return False # Token is not from our webpage

    tokenTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(tokenData['exp']))); # epoch to date
    currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime());

    if tokenTime < currentTime:
        return False

    return True

@get('/token')
def token():
    global config 

    state    = str(request.GET.get('state'))
    userCode = str(request.GET.get('code'))

    # Confirm that the state received from Google matches 
    # the session token we created

    if state == config['state']:

        token_endpoint  = getTokenEndPoint(); 
        tokenDictionary = getEncryptedToken(token_endpoint, userCode)
        id_token        = tokenDictionary['id_token']
        tokenData       = getTokenData(id_token); # Dictionary with the token information (including email and so)

        if (validateToken(tokenData)):
            profile = {
                'email' : tokenData['email']
            }
            return template('welcome', profile=profile);
        else:
            return "BOOOOO. You're a hacker!!. Tokens not valid"

if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)
