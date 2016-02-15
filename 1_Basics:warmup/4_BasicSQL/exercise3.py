import sqlite3

dbfile = "managmentSystem.sqlite3"

#t = table's name | f = filename
t_university    = "University"
f_university    = "./dbFiles/universities.txt"
t_students      = "Students"
f_students      = "./dbFiles/students.txt"
t_aplications   = "Aplications"
f_aplications   = "./dbFiles/solicitudes.txt"

# DB configuration
def config(dbfile):
	conn   = sqlite3.connect(dbfile)
	cursor = conn.cursor()
	return conn, cursor

config = config(dbfile);
conn   = config[0]
cursor = config[1]

def firstQuery(cursor):

	print "\nQuery 1: Correction value less than 1000 and Computers science at the Complutense University of Madrid\n"
	
	try:
		cursor.execute('Select Nombre_Est, Nota, Decision FROM Students JOIN Aplications ON Students.ID=Aplications.ID WHERE Students.Valor<1000 AND Aplications.Nombre_Univ="Universidad Complutense de Madrid" AND Aplications.Carrera="Informatica"')
		
		for line in cursor:
			print "\t" + line[0] + ", " + str(line[1]) + ", " + line[2]
	
		print "\n\tFirst query completed successfully...[OK]\n"

	except:
		print "\n\tFirst query wasn't completed successfully...[ERROR]\n"

def secondQuery(cursor):

	print "Query 2: Students whose weighted rating changes 1 or more the original\n"
	try:
		cursor.execute('Select Nombre_Est, Nota, Valor FROM Students')
		#Not necessary: lineList = [] #List of student that have (nota-(nota*valor/1000))>1 

		for line in cursor:

			mark 			= line[1]
			correctionValue = line[2]
			weightedMark 	= (mark * correctionValue) / 1000;
			total 		= abs(mark - weightedMark) #Nota-ponderada=Nota*Valor de correccion/1000 

			if (total > 1):
				print "\t" + line[0] + " weighted mark differs in " + str(total)
		
		print "\n\tSecond query completed successfully...[OK]\n"

	except IOError:
		print IOError
		print "\n\tProblems calculating weighted mark...[ERROR]\n"

def thirdQuery(cursor):
	noApliedStudents = []

	try:
		sqlquery = """SELECT * FROM Students WHERE Students.ID not IN \
					  (Select Students.ID FROM Students JOIN Aplications WHERE Students.ID=Aplications.ID)"""

		cursor.execute(sqlquery); # Execute the query in order to get in cursor all the students that id doesn't appear on the aplications table
		
		for line in cursor:
			lineList = []
			lineList.append(line[0]); #ID
			lineList.append("Universidad de Jaen"); #Name
			lineList.append("Informatica"); #Carrera
			lineList.append("Si"); #Insert also the decition for the aplications 
			noApliedStudents.append(tuple(lineList));

		for entry in noApliedStudents:
			cursor.execute("INSERT INTO Aplications values (?, ?,?,?) ", (entry[0], entry[1], entry[2], entry[3]) );
		
		print "Third query completed successfully...[OK]"

	except:
		print "Third query: database was previously updated with this data... [NOT INSERTED]"

def fourthQuery(cursor):
	aplications = []

	try:
		#Devolver todos los estudiantes que querian estudiar economicas pero que no fueron admitidos en la unviersidad
		cursor.execute("SELECT * FROM Aplications WHERE Aplications.Decision='No' AND Aplications.Carrera = 'Economia' ");

		for entry in cursor:
			newAplication = []
			newAplication.append(entry[0]); #ID
			newAplication.append("Universidad de Jaen"); #Name
			newAplication.append("Economia"); #Carrera
			newAplication.append("Si"); #Insert also the decition for the aplications
			aplications.append(newAplication);

		#Insertar nuevas entradas admitiendoles en la universidad de jaen	
		for row in aplications:
			cursor.execute("INSERT INTO Aplications values (?, ?,?,?) ", (row[0], row[1], row[2], row[3]) );
		
		#cursor.execute("insert into University values (?, ?, ?) ", ("Universidad de Jaen", "Jaen", 1000));

		print "Fourth query completed successfully...[OK]"

	except:
		print "Fourth query: database was previously updated with this data... [NOT INSERTED]"

"""Borrar a todos los estudiantes que solicitaron mas de 2 carreras diferentes."""

def fithQuery(cursor):
	duplicatedAplicationsID =  []
	duplications = ""

	sqlquery = """
	SELECT ID, COUNT(*)
	FROM Aplications
	GROUP BY
	    ID
	HAVING 
	    COUNT(*) > 1
	"""

	try:

		cursor.execute(sqlquery);

		# Iterate on the query with cursor and save the value on a list
		for l in cursor: 
			duplications += (str(l[0]) + ", ")
			duplicatedAplicationsID.append(l[0]);

		for d in duplicatedAplicationsID:
			statement = "DELETE FROM Aplications WHERE ID IN (" + str(d) + ")"
			cursor.execute(statement);
		
		print "Fith query completed successfully...[OK]"

	except:
		print "Fith query: problems deleting database entries... [NOT DELETED]"

firstQuery(cursor);
secondQuery(cursor);
thirdQuery(cursor);
#fourthQuery(cursor);
#fithQuery(cursor);

conn.commit() # Update changes to database
cursor.close()

