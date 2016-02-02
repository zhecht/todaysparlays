import MySQLdb
import constants




def makeCursor():
    db = MySQLdb.connect(
	    host = constants.HOST_CONST,
	    user = constants.USER_CONST,
	    passwd = constants.PASSWRD_CONST,
	    db = constants.DB_CONST
	)
    return db.cursor()

def getRecord(name, sport):
	tmp = ""
	cursor = makeCursor()

	cursor.execute("SELECT CB_Record FROM NCAA WHERE name=%s", [name])
	return cursor.fetchone()

def getStreak(name, sport):
	tmp = ""
	cursor = makeCursor()
	if sport == "NCAAB":
		tmp = "CB_Record"
	elif sport == "NCAAF":
		tmp = "CF_Record"

	cursor.execute("SELECT CB_Streak FROM NCAA WHERE name=%s", [name])
	return cursor.fetchone()

def getNBAStats(name):
    cursor = makeCursor()
    cursor.execute("SELECT * FROM NBA WHERE name=%s", [name])
    return cursor.fetchall()

def getNCAAStats(name, sport):
    cursor = makeCursor()
    if sport == "NCAAB":
		cursor.execute("SELECT CB_Record,CB_Streak FROM NCAA WHERE name=%s", [name])
    else:
		cursor.execute("SELECT CF_Record,CF_Streak FROM NCAA WHERE name=%s", [name])
    return cursor.fetchall()

def get_NCAA_DB_Name(name):
    cursor = makeCursor()
    db_name = ""
    name_split = name.split(" ")
    if name_split[-1] == "U":
        count = 0
        for n in name_split:
			if n == "U":
				return db_name
			elif count != 0:
				db_name += " "

			db_name += n.lower()
			count += 1
    elif name == "Arkansas LR":
		db_name = "arkansas-little rock"
    elif name == "Minnesota U":
	    db_name = "minnesota"
    elif name == "ST John's":
		db_name = "st. john's"

    elif name == "Loyola":
		if name_split[0] == "Chicago":
			db_name = "loyola (IL)"
		elif name_split[0] == "Maryland":
			db_name = "Loyola (MD)"
		else:
			db_name = "Loyola Marymount"

    elif name_split[0] == "Miami":

		if name_split[1] == "Ohio":
			db_name = "Miami (OH)"
		else:
			db_name = "Miami (FL)"
    elif name == "St Joseph's":
		db_name = "Saint Joseph's (PA)"
    elif name == "NC State":
		db_name = "North Carolina State"
    elif name == "Cal Santa Barbara":
		db_name = "UC Santa Barbara"
    else:
		db_name = name
    return db_name.lower()

def get_public(name, sport):
	cursor = makeCursor()

	if sport == "NCAAB" or sport == "NCAAF":
		cursor.execute("SELECT CB_PERCENT, CB_LINK FROM NCAA WHERE name=%s", [name])
	elif sport == "NBA":
		cursor.execute("SELECT PERCENT, LINK FROM NBA WHERE name=%s", [name])

	#print cursor.fetchall()
	return cursor.fetchall()

def getNFLStats(name):
    cursor = makeCursor()
    cursor.execute("SELECT * FROM NFL WHERE name=%s", [name])
    return cursor.fetchall()

