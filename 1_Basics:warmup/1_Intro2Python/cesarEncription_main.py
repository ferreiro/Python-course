# Chechinput: returns false is the inputed text 
# has any numeric character

def checkInput(userInput):
	valid = True

	for char in userInput:
		if (char == "" or char == " "):
			continue
		else:
			isNumber = checkNumber(char)
			valid &= not isNumber

	return valid
 
# CheckNumber: returns false is the inputed text 
# has any numeric character

def checkNumber(userInput):
	if "0" <= userInput <= "9":
			return True
	else:
		return False
	
''' Returns 1 if its a letter and is on the alfhabet (a, b, c ... z)'''
def checkSymbol(letter):
	
	auxLetter = letter.lower() 
	if "a" <= auxLetter <= "z":
		return True
	else:
		return False

# Reads a valid message from the user
# and returns to the user.

def readMessage():
	message = '';
	valid = False; 
	while(not valid):
		# Iterate until input message has not have any numeric element (number)
		message = raw_input('> Introduce your message: ');
		valid = checkInput(message);
		if (not valid):
			print '\t Come on! Numbers are not permited in this program :P'; 

	return message;

# Now, let the user inputs the desired shift number
# iterates until inputed number is correct.

def readNumber():
	number = -1;
	valid = False;
	while(not valid):
		number = raw_input('> Introduce your shift Number: ');
		valid = checkNumber(number);
		if (not valid):
			print '\t Come on! this is not a number :P'; 

	return number;

# Reads a message and a number from the user
# and returns and object composed of a message and a number.

def userInput(): 
	message = readMessage();
	number = readNumber(); 

	# Compose and object and returns to the user
	userInput = {
		'message': message, 
		'number': number
	};

	return userInput;

# Character to Number: Converts a given integer to 
# corresponding character on ASCII code.

def characterToNumber(char):
	number = -1;
  	
	if (char == 'z' or char == 'Z'):
		if (char == 'z'):
			number = ord('a');
		elif (char == 'Z'):
			number = ord('A');
		number -= 1;
	else:
		number = ord(char); # Character to Number

	return number;

def simpleEncription(message, shiftNumber):

	if (type(shiftNumber) is not int):
		shiftNumber = int(shiftNumber); # Int casting of shiftNumber when typed is not expressed as integer. Sometimes may ocurr the program interprets a string...
	
	auxChar = '';
	encriptedMsg = list();
	shiftNumber = shiftNumber % 26; # English alfhabet has 26 elements. when user shifs more than 26, then make the modulus! if not, an error will crash lines below.
	tmpNum = 0;

	# Convert each character of the array into a
	# number, then sum the shif and finally convert this
	# number into the alfabhet letter corresponding.
	
	for char in message:

		tmpNum = characterToNumber(char);

		if checkSymbol(char):
			tmpNum += shiftNumber; # Add shift number to the character number on Ascii
		# else: It's an space. Don't do anything"			
		
		encriptedChar = chr(tmpNum); # Convert from number to char.
		encriptedMsg.append(encriptedChar); # Add encripted message to the list

	return encriptedMsg;

# Main program

userInput = userInput(); # Returns a valid message and shif number from user in a list.
message = userInput['message']; # Local variable for the message inputed by the user
number = userInput['number']; # Local variable for the number inputed by the user

encriptedMsgList = simpleEncription(message, number);
outputMsg = '';

for index, char in enumerate(encriptedMsgList):
	outputMsg += char;

print outputMsg
