# -*- coding: utf-8 -*-
import csv
import time

filename 			 = "PitchingPost.csv"
filenameAcummYears 	 = "AcumAnnos.csv"
filenameAcummPlayers = "AcumJugadores.csv"
filenameOrdered 	 = "Ordenado.csv"

""" Create a .csv file given a header, content of the csv and outputf filename """

def writeFile(headerList, data, outputFile):
	success = True; # 0 means success | -1 = fails writing the file

	#TODO: Check if the file has .csv format. If not. Will return false
	try:
		outputFile = open(outputFile, 'w')
		csvWriter = csv.writer(outputFile, delimiter=',', dialect='excel'); # http://stackoverflow.com/questions/29335614/python-csv-writer-leave-a-empty-line-at-the-end-of-the-file	 	
	 	csvWriter.writerow(headerList); # write the header to the csv file
	 	
	 	for index, player in enumerate(data):
			csvWriter.writerow(player);

		outputFile.close();

	except:
		return False; # We couldn't write on the file

	return success;

def readCSV(inputFilename):

	if not inputFilename.endswith(".csv"): # Check if the file has .csv format. If not. Will return false
		print "Outpufile extension %s not valid" % (outputFile[-4:]) # Notify file output extension doesn't exist
		print successMsg + "[ERROR]"
		return None; # return a null object
	
	try:
		fs = open(inputFilename) 
		reader = csv.reader(fs)
		contacts = list(reader) # Load all the contacts from the .csv to a contacts array.
		fs.close(); # close the file manager
	except:
		return None;

	return contacts;

def convertDictToList(inputDictionary):

	if (not isinstance(inputDictionary, dict)): 
		return None; #is not a Dictionary

	newList = [] # it's a Dictionary

	for key, value in inputDictionary.iteritems():
		aux = [key, value]
		newList.append(aux);

	return newList; # correct conversion

""" Returns False if wasn't possible to create a year frecuency table
	When success, returns True """

def createYearFrecuencyFile(inputFilename, outputFilename):

	success 	   = True;	
	frecuency  = {} # dictionary to save the frecuncy for each year

	try:
		playersList = readCSV(inputFilename); # Loads player list from .csv file

		for index, player in enumerate(playersList):

			if index >= 1: # starts on 1 to skip the csv header
				year = str(player[1]) # index = 1, is the year field on csv

				if year in frecuency:
					frecuency[year] += 1; # Player was previously added to the dictionary. Increase value by one
				else:
					frecuency[year] = 1; # Hashtag wasn't in the directionary. Add it with 1 value				
	except:
		return False

	headerList = ["year", "frecuency"] # header to write on the .csv file
	yearFrecuencyList = convertDictToList(frecuency);

	if (yearFrecuencyList == None): return False

	if not writeFile(headerList, yearFrecuencyList, outputFilename): # export list to output file 
		print "Error writing a file"
		return False; # problems writing to a file
	
	return success; # Success

""" Returns False if we coudn't create the output file.
	And success when creates a player frecuency table 
	in a given output filename """

def createPlayerFrecuencyFile(inputFilename, outputFilename):

	success = True; # returned value
	playerFrecuency = {} # dictionary to save the frecuency for each Player

	try:
		playerList = readCSV(inputFilename); # loads player list from .csv file

		for index, player in enumerate(playerList):
			
			if(index >= 1): # starts on 1 to skip the csv header	
				PlayerID = str(player[0]) # index = 0, is the PlayerId field on csv
				
				if PlayerID in playerFrecuency:
					playerFrecuency[PlayerID] += 1; # Player was previously added to the dictionary. Increase value by one
				else:
					playerFrecuency[PlayerID] = 1; # Hashtag wasn't in the directionary. Add it with 1 value				

	except:
		print "%s file with bad format or not existing" % (inputFilename)
		return False; # Coudn't read the input file

	headerList 			= ["player", "frecuency"] # header to write on the .csv file
	playerFrecuencyList = convertDictToList(playerFrecuency);
	
	if (playerFrecuencyList == None): return False
	
	if not writeFile(headerList, playerFrecuencyList, outputFilename): # export list to output file 
		print "Error writing a file"
		return False; # problems writing to a file

	return success;

""" Order a list of player loaded from a .csv file 
	and then create a new file with this ordered player list """

def createOrderPlayerFile(inputFilename, outputFilename):

	success = True

	try:
		csvFile 	= readCSV(inputFilename); # loads player list from .csv file
		headerList 	= csvFile[0]; # Header like Name,ID... to write the .csv
		playerList  = sorted(csvFile[1:]); # sorted player list (without header)
		writeFile(headerList, playerList, filenameOrdered); # Write the heade
	except:
		return False; # Read from CSV or write to output file fails

	return success;

# start_time = time.time()
if (createOrderPlayerFile(filename, filenameOrdered)): print "Sorted player's list created...[OK]"
else: "Sorted player's list created...[ERROR]"
# print("--- %s seconds ---" % (time.time() - start_time))

# start_time = time.time()
if (createYearFrecuencyFile(filename, filenameAcummYears)): print "Year frecuency list created...[OK]"
else: "Year frecuency list create[ERROR]"
# print("--- %s seconds ---" % (time.time() - start_time))

# start_time = time.time()
if (createPlayerFrecuencyFile(filename, filenameAcummPlayers)): print "Player frecuency list created...[OK]"
else: "Player frecuency list create[ERROR]"
# print("--- %s seconds ---" % (time.time() - start_time))

