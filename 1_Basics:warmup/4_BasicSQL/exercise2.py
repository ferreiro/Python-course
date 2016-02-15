import sqlite3

dbfile = "managmentSystem.sqlite3"

# t = table's name | f = filename
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

# Inserting data into the database

def insertFromFile(filename, table, cursor, conn):

	try:
		fileManger = open(filename)
		rows = [line.rstrip().split(',') for line in fileManger]
		rows = [str(tuple(rec)) for rec in rows]

		for row in rows:
			cursor.execute('insert into ' + table + ' values ' + row)
	except:
		print "We couldn't insert information into the database"
		
	if (conn): conn.commit()

insertFromFile(f_university, t_university, cursor, conn)
insertFromFile(f_students, t_students, cursor, conn)
insertFromFile(f_aplications, t_aplications, cursor, conn)

cursor.close()

