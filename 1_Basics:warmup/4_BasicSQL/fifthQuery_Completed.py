

def fithQuery2(cursor):
	#idea find all id of student and for all student search on the aplication tabla and obtain only the carrera
	#if the Distincs carrera for each student is more than 2 borra ello
	aplications = []
	try:
		cursor.execute('Select ID FROM Students')
		lineList =[] #list of all id of students
		for line in cursor:
			lineList.append(line[0]) #find a way to pass the id of the student that are in lineList to serch for all the student
		for line in lineList:
			i=0
			cursor.execute("SELECT DISTINCT Carrera FROM Aplications WHERE Aplications.ID= %s",lineList[i]) 
			#cursor.execute("SELECT DISTINCT Carrera FROM Aplications WHERE Aplications.ID='345'") 
			for line in cursor:
				aplications.append(line[0])
				print str(line[0])

			if(len(aplications)>2):
				print str(len(aplications))
				#Student that have request more than 2 different carreras
				cursor.execute("DELETE From Aplications WHERE Aplications.ID='lineList[i]'")
				#cursor.execute("DELETE From Aplications WHERE Aplications.ID='345'")
				print "cancel from database"
				conn.commit()
			i=+1

		#cursor.execute('Select ID,Nombre_Univ,Carrera,Decision FROM Aplications')
		#print "last query result:"
		#for line in cursor:
		#	print str(line[0]) + ", " + line[1]+ ", " + line[2]+ ", " + line[3]

		print "Fith query completed successfully...[OK]"

	except:
		print "Fith query: problems deleting database entries... [NOT DELETED]"