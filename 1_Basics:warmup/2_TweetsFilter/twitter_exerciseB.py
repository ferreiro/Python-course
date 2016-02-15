# -*- coding: utf-8 -*-
import csv
import json

outdirectory 	= "outputCSV/"
tweetsFile 		= "tweets.txt";
outputFile 		= "mostUsedHasgtags.csv";

tweetsList = [] # List that contains all the tweets readed from a file
hashtagTable = {}; # Dictionary with key= hashtags and value= frecuency for this hashtag 

""" Returns a list of tweets readen from a file.
	if there's a problem None object will be returned """

def loadTweets(inputFilename):

	tweetsList = [] # returns a list of tweets

	try:
		openedFile = open(inputFilename, "r");
		
		for line in openedFile:
			tweet = json.loads(line);
			if not tweet.has_key('delete'):
				tweetsList.append(tweet);
			# else: skip objects with "delete" key

		openedFile.close(); # Close the file

	except:
		return None;

	return tweetsList;

""" Creates a hasmap frecuency table where keys are the hashtags and
	values are the number or appeareances of that hashtag in all the twetts.
	Returns None if we coudn't create the Hashmap and a dictionary if everything works"""

def createHashtagFrecuencyTable(inputList):

	if (not isinstance(inputList, list)): 
		return None; # exit function if the input object is not a list

	try:
		hashtagTable = {} # create empty dictionary

		for tweet in inputList: # iterate all the tweets loaded in the list
			for hashtag in tweet['entities']['hashtags']: # iterate all the hastags for each tweet
				
				hashtagName = hashtag['text']; # Get a hashtag from the weet

				if (hashtagName in hashtagTable): 
					hashtagTable[hashtagName] += 1; # Hashtag was previously added to the dictionary. Increase value by one
				else:
					hashtagTable[hashtagName] = 1; # Hashtag wasn't in the directionary. Add it with 1 value

	except: 
		return None;

	return hashtagTable

""" Returns a ordered hasmap, where the sorting was made taking into acccount
	the value of each key on the hasmap and desdending order. """

def orderHashtagTable(dictionary):
	if (not isinstance(dictionary, dict)): 
		return None; # exit function if the input object is not a dictionay

	return sorted(dictionary.items(), key = lambda t:t[1], reverse=True); # INFO: https://www.youtube.com/watch?v=MGD_b2w_GU4

""" This function writes header and data to a .csv file pass by value
	If the outputFile passed is not a .csv type. A failure will returned (False) """

def writeFile(headerList, data, outputFile):
	
	success = True; # 0 means success | -1 = fails writing the file

	if not outputFile.endswith(".csv"): # Check if the file has .csv format. If not. Will return false
		
		print "Outpufile extension %s not valid" % (outputFile[-4:]) # Notify file output extension doesn't exist
		return False; # output file format not valid
	
	try:

		outputFile 	= open(outputFile, 'w')
		csvWriter 	= csv.writer(outputFile, delimiter=',', skipinitialspace=True, dialect='excel'); # http://stackoverflow.com/questions/29335614/python-csv-writer-leave-a-empty-line-at-the-end-of-the-file	 	
	 	csvWriter.writerow(headerList); # write the header to the csv file

	 	for hashtag in data:
	 		csvWriter.writerow(hashtag);
	 	
		outputFile.close();

	except:
		return False; # Problems writting the file

	return success;


tweetsList = loadTweets(tweetsFile); # Loading a list of twetts from a file

if (tweetsList != None): print "Loading twetts from file...[OK]"
else: "Loading twetts from file...[ERROR]"

hashtagTable = createHashtagFrecuencyTable(tweetsList);

if (hashtagTable != None): print "Creating hashtags table with its frecuencies...[OK]"
else: "Creating hashtags table with its frecuencies...[ERROR]"

orderedHashtagTable = orderHashtagTable(hashtagTable)

if (orderedHashtagTable != None): print "Ordering hashtags table in desdending order...[OK]"
else: "Ordering hashtags table in desdending order...[ERROR]"

headerList = ["hashtag", "frecuency"] # .csv header to write on the file

if (writeFile(headerList, orderedHashtagTable[:10], outputFile)): print "Writing csv file with top used hashtags...[OK]"
else: "Writing csv file with top used hashtags...[ERROR]"


