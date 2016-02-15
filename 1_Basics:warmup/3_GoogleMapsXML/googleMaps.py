# -*- coding: utf-8 -*-
import xml
import urllib
from xml.etree import ElementTree

googleAPI = "http://maps.googleapis.com/maps/api/geocode/xml?"
place = {
	"name": None, 
	"country": None,
	"address": None,
	"short_name": None, 
	"level_1_entity": None, 
	"latitude": None, 
	"longitude": None 
}

# Google api specific attribute
def checkValidTree(tree):
	if (tree[0].tag == "status" and tree[0].text == "OK"): 
		return 0
	else:
		return -1

def displayPlaceInformation(data):
	print "| Information"
	print "Name: %s" % data['name']
	print "Country: %s" % data['country']
	print "Short name of Country: %s" % data['short_name']
	print "Level 1 entity: %s" % data['level_1_entity']	
	print "Formated adress: %s" % data['address']
	print "Latitude %f Longitude: %f" % (float(data['longitude']), float(data['latitude']))

''' Returns -1 when the data is not valid.
	0 in other cases '''

# http://stackoverflow.com/questions/1912434/how-do-i-parse-xml-in-python

def parsingXML(data, place):

	tree  = ElementTree.fromstring(data)
	valid = checkValidTree(tree);

	if valid == -1:
		
		print "The XML is not valid"

	else:

		addresses 	 = [] # List of "Dictionaries" with all the adresses from google api (first, local, etc)
		root  		 = tree[1] # The 1 element in the array is the api result that we're going to parse

		# Iterating through all the XML nodes and check if the're 
		# Some node we're interested in

		for elem in root:

			if elem.tag == 'address_component':
				adressesDict = {} # Single adress to be stored on adresses list

				for children in elem: 
					adressesDict[children.tag] = children.text
					
				addresses.append(adressesDict) # Add the adress dict to the adresses list

			elif elem.tag == 'formatted_address':
				place['address'] = elem.text # save formated addres on the python dictionary
			
			elif(elem.tag == 'geometry'):
				location = elem.find('location') # Find the location element inside all the geometry tags
				place['latitude'] = location.find('lat').text # Get latitud value of the object
				place['longitude'] = location.find('lng').text

		# Setting the city dictionary with the values we
		# are interested in 

		place['name'] = addresses[0]['long_name']
		place['country'] = addresses[-1]['long_name']
		place['short_name'] = addresses[-1]['short_name']
		place['level_1_entity'] = addresses[-2]['long_name']
		
def callAPI(address, googleAPI):

	parameters = urllib.urlencode({'address': address });
	url  = googleAPI + parameters

	# print "Calling " + url

	uh 	 = urllib.urlopen(url)
	data = uh.read();

	return data

''' Returns a string for the city inputted by the user '''
def introduceCity():
	valid = False

	while not valid:
		city = raw_input("Introduce your data: ")
		if city: # and city.isalpha()
			valid = True
		else:
			print '\t Come on! Numbers are not permited in this program :P'; 

	return city

def main():
	global place
	stop = False

	while not stop:

		city = introduceCity()

		if  city == 'stop':
			stop = True # exit the program
		else:
			returnedData = callAPI(city, googleAPI);
			parsingXML(returnedData, place)
			displayPlaceInformation(place)

	print "Exiting the program"

main()
