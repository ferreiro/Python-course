import sqlite3

conn   = sqlite3.connect('managmentSystem.sqlite3')
cursor = conn.cursor()

def createUniversityTable(cursor):
	cursor.execute("DROP TABLE IF EXISTS University")
	cursor.execute("CREATE TABLE University(Nombre_Univ TEXT, Comunidad TEXT, Plazas INTEGER, PRIMARY KEY(Nombre_Univ))")

def createStudentTable(cursor):
	cursor.execute("DROP TABLE IF EXISTS Students")
	cursor.execute("CREATE TABLE Students(ID TEXT, Nombre_Est TEXT, Nota REAL, Valor INT, PRIMARY KEY(ID))")
	
def createApplicationsTable(cursor):
	cursor.execute("DROP TABLE IF EXISTS Aplications");
	cursor.execute("CREATE TABLE Aplications(ID TEXT, Nombre_Univ TEXT, Carrera TEXT, Decision TEXT, PRIMARY KEY(ID, Nombre_Univ, Carrera), FOREIGN KEY(Nombre_Univ) REFERENCES University(Nombre_Univ), FOREIGN KEY(ID) REFERENCES Students(ID))");

def createDatabase(cursor):
	createUniversityTable(cursor)
	createStudentTable(cursor)
	createApplicationsTable(cursor)

createDatabase(cursor)
conn.commit()
cursor.close()