import os
import json

# Global variables

path = "./files/"
filename = "agenda.json"
agenda   = {} #dictionary for saving all agenda (contacts, whatever)
messages = {
	"system" : "[ System ]",
	"warning" : "[ Warning ]",
	"problem" : "[ Problem ]",
	"success" : "[ OK ]",
	"fail" : "[ ERROR ]"
}

# Load users from JSON into a dictionary
def loadUsers(filename):
	global messages
	global agenda
	global path

	try:
		fileURL = path + filename
		data = open(fileURL, 'r'); # try to open JSON file
		jsonData = json.load(data) # parse json object into python dictionary
		agenda = jsonData # save agenda object into global variable "agenda"
		# print messages['system'] + " Contacts loaded"
	except:
		agenda['contacts'] = [] # set empty dictionary
		print messages['warning'] + " Problems... File not exist or BAD FORMAT!"
		print messages['system'] + " We're creating an empty list\n"

def saveUsers(filename):
	global messages
	global agenda
	global path

	if agenda == None or agenda == {}:
		# When the agenda is empty or None. We create an empty contacts array
		# print messages['warning'] + " No object is created.\nWe're going to save and empty object\n"
		agenda['contacts'] = [] # empty array for contacts

	json_array = json.dumps(agenda) # Converts agenda dictionary into JSON format.
	
	try:
		
		# Save agenda into json file. First we check if the folder exists. And then save the file in that destination
		if not os.path.exists(path): os.makedirs(path) # create a new "folder" called files if not exists.
		fileURL = path + filename
		fileManager = open(fileURL, 'w');
		fileManager.write(json_array);
		
		# print messages['success'] + " Contacts saved in agenda..."
	
	except:

		print messages['warning'] + " Problems saving the file"

""" Create user: add an user to the database only if the user is not already created in our system. In other case, will return false """
def createUser(user):
	global messages
	global agenda

	created = True
	
	if agenda == None or agenda == {}:
		
		# If agenda empty or doesn't exit. Creating a new contacts field on dictionary agenda and add the user
		agenda = {} # Agenda is empty, so create a new contacts field
		tmpContacts = []
		tmpContacts.append(user);
		agenda['contacts'] = tmpContacts # saving on dictionary
		print "\n" + messages['success'] + " User added to the agenda \n"
	
	else:

		contacts = agenda['contacts']

		if not existContact(user):
			contacts.append(user)
			print "\n" + messages['success'] + " This user is not on our database. We're adding it ;-)"
		else:
			created = False
			print "\n" + messages['warning'] + " Not added! This user is already on the Database"

""" 
	User index returns -1 if the user is not found on the database. In other cases, returns the index on the array.
	We use an extra bool parameter called 'allFieldsRequired', this is use When
	we want to know if all the fields for a user (name, surname and phone) is on our database.
	When this field is false, means that we only want to check if some of the values of the user is on our database.
"""
def userIndex(user, contacts, allFieldsRequired):
	
	index = -1 # Return variable. -1 == Not found
	found = False
	i = 0

	while not found and i < len(contacts):
		# phone is going to be my primary key (Two users can't have the same phone)
		
		if (allFieldsRequired):
			if(contacts[i]['name'] == user['name'] and contacts[i]['surname1'] == user['surname1'] and contacts[i]['surname2'] == user['surname2'] and contacts[i]['phone'] == user['phone']):
				found = True
				index = i
		else:
			if(contacts[i]['name'] == user['name'] or contacts[i]['surname1'] == user['surname1'] or contacts[i]['surname2'] == user['surname2'] or contacts[i]['phone'] == user['phone']):
				found = True
				index = i

		i += 1;

	return index
 
def existContact(user):
	global agenda

	contacts = agenda['contacts']
	index = userIndex(user, contacts, True);
	
	if (index == -1):
		return False
	else:
		return True

def updateUser(user):
	global agenda

	updated = True
	contacts = agenda['contacts']
	index = userIndex(user, contacts, True)

	if (index != -1): 
		contacts[index]['name'] = user['name']
		contacts[index]['phone'] = user['phone']
		contacts[index]['surname1'] = user['surname1']
		contacts[index]['surname2'] = user['surname2']
	else:
		updated = False # user doesn't exist

	return updated

def deleteUser(user):
	global agenda

	deleted = False
	contacts = agenda['contacts']
	index = userIndex(user, contacts, True);

	if index >= 0:
		contacts.pop(index)
		deleted = True

	return deleted

def deleteLastUser():
	global agenda

	contacts = agenda['contacts']
	deleted = False

	if len(agenda['contacts']) >= 1:
		deleted = True
		contacts.pop();

	return deleted;

""" Clear the command line """
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

""" Returns a dictionary with a readed user """
def introduceUser():
	name = raw_input("name: ");
	surname1 = raw_input("surname1: ");
	surname2 = raw_input("surname2: ");
	phone = raw_input("phone: ");

	newUser = {
		"name" : name,
		"surname1" : surname1,
		"surname2" : surname2,
		"phone": phone
	}

	return newUser

def printUser(user):
	print 'Name: ' + str(user['name'])
	print 'Phone: ' + str(user['phone'])
	print 'Surname1: ' + str(user['surname1'])
	print 'Surname2: ' + str(user['surname2']) 
	
def search():
	global agenda

	contacts = agenda['contacts']

	print "What do you want to Search?"
	print "Valid answers: name, phone, surname1, surname2"

	valid = False
	toSearch = ""
	user = {
		"name" : "",
		"surname1" : "",
		"surname2" : "",
		"phone" : ""
	}

	while not valid:
		
		toSearch = raw_input("Search by : ")
		toSearch.lower()
		valid = True

		if (toSearch == "all"):
			valid = True
			user = introduceUser()
			index = userIndex(user, contacts, True)

		elif (toSearch == "name"):
			user['name'] = raw_input("What is the name? ");
		
		elif (toSearch == "phone"):
			user['phone'] = raw_input("What is the phone? ");
			
		elif (toSearch == "surname1"):
			user['surname1'] = raw_input("What is the surname1? ");

		elif (toSearch == "surname2"):
			user['surname2'] = raw_input("What is the surname2? ");
		else:
			valid = False

	if (toSearch != "all"): 
		index = userIndex(user, contacts, False)
	
	if (index != -1):
		print messages['success'] + " User found!"
		printUser(contacts[index])
	else:
		print messages['fail'] + " User is not found"
 
""" Returns a user created by the user """
def introduceSearch():
	user = {}
	name = "";
	surname1 = "";
	surname2 = "";
	phone = "";

	the_name = raw_input("Search by name?: [yes/no]")
	if (the_name == "yes"): name = raw_input("Name: ");
	
	the_phone = raw_input("Search also by phone?: [yes/no]")
	if (the_phone == "yes"): phone = raw_input("phone: ");

	surname = raw_input("Search also by surname 1?: [yes/no]")
	if (surname == "yes"): surname1 = raw_input("surname 1: ");

	surname = raw_input("Search also by surname 2?: [yes/no]")
	if (surname == "yes"): surname2 = raw_input("surname 2: ");

	user = {
		"name" : name,
		"surname1" : surname1,
		"surname2" : surname2,
		"phone": phone
	}

	return user

def displayContacts():
	global agenda

	print "Agenda:"
	for c in agenda['contacts']:
		print "------"
		printUser(c)

def menu():
	option = ""

	print "----------- MENU -----------" 
	print "create (create entry)"
	print "delete (delete the last one entry)"
	print "deleteUser (delete one user)"
	print "display (delete one user)"
	print "search (search entry)"
	print "exit (close program)"
	print "----------------------------" 

	return str(raw_input("Your option? ")).lower()

def main():
	global agenda
	global filename

	cls() # clear the screen
	exit = False
	loadUsers(filename) # load users

	while not exit:

		# print agenda['contacts']
		option = menu()
		cls() # clear the screen 

		if (option == "exit"):
			exit = True

		elif (option == "create"):
			newUser = introduceUser()
			createUser(newUser)

		elif (option == "delete"):
			if (deleteLastUser()):
				print messages['success'] + " user deleted!"
			else:
				print messages['warning'] + " user not deleted because there are not any user on the DB!"

		elif (option == "deleteuser"):

			user = introduceUser()
			deleted = deleteUser(user)

			if (deleted):
				print messages['success'] + " user deleted!"
			else:
				print messages['warning'] + " user not deleted because there are not any user on the DB!"

		elif (option == "display"):
			displayContacts()

		elif (option == "search"):
			search()

		else:
			print "Error. Command not found"

	saveUsers(filename) # load users


main()
