from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib2
import MySQLdb
import constants



def soupify(html):
	return BeautifulSoup(html, "lxml")

def get_html(url):
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	con = urllib2.urlopen(req).read()
	#con = open("record.txt")

	#print con
	return con


def get_teams(sport, html):

	soup = soupify(html)

	teams = []

	for tbody in soup.find_all("tbody"):
		i = 0
		for tr in tbody.find_all("tr"):

			team = tr.find("span")

			if team != None:
				team = team.text.lower()

				teams.append(team)
	return teams

def p(z):
	for i in z:
		print i
		print "\n"

def get_record(sport, html):


	soup = soupify(html)

	records = []

	counter = 0
	nfl = False
	if sport == "NCAAF":
		nfl = True


	for tbody in soup.find_all("tbody"):
		i = 0

		#p(tbody.find_all("tr"))

		for tr in tbody.find_all("tr"):

			col = 0
			wins = ''
			losses = ''
			streak = ''
			rec = ''
			PA = 0
			PF = 0
			total_games = 0


			# good luck reading this later
			#if i != 0 and ((nfl == True and counter == 0 and i != 8) or (nfl == True and counter == 2) or (nfl == True and counter == 5) or (nfl == True and counter == 10) or (nfl == True and counter == 1 and i != 7) or (nfl == True and counter == 3 and i != 8) or (nfl == True and counter == 4 and i != 8) or (nfl == True and counter == 6 and i != 7) or (nfl == True and counter == 7 and i != 7) or (nfl == True and counter == 8 and i != 7) or (nfl == True and counter == 9 and i != 8)):
			if i != 0 and ((nfl == False and counter == 16 and i != 7) or (nfl == False and counter == 21 and i != 7) or counter != 16 or counter != 21):
				#round 2
				

				for td in tr.find_all("td"):


					if col == 0:


						team = td.findChildren()


						if team != None and len(team) != 0:
							#print team
							#print team.findChildren()
							team = team[-1].text.lower()
							#print team

					#print team

					if team == None:
						#nothing
						a = ""
					elif sport == "NCAAF":

						if col == 2:
							rec = td.text
							wins_s = rec.split("-")

							wins = int(wins_s[0])
							losses = int(wins_s[1])
							total_games = wins + losses
						elif col == 3:
							pf = int(td.text)
							PF = float(pf / total_games)
						elif col == 4:
							pa = int(td.text)
							PA = float(pa / total_games)
						elif col == 7:
							streak = td.text
					else:
						if col == 4:

							wins = td.text
						elif col == 5:

							losses = td.text
						elif col == 7:

							streak = td.text


					col += 1

				if sport == "NCAAB":

					records.append({'team': team, 'wins': wins, 'losses': losses, 'streak': streak})
				else:

					records.append({'team': team, 'rec': rec, 'streak': streak, 'PF': PF, 'PA': PA})

					if team == "louisiana-monroe":

						return records

			i += 1


		counter += 1

	return records


	

def updateRecords(sport, url):

	html = get_html(url)
	teams = get_teams(sport, html)
	records = get_record(sport, html)

	
	#print records
	#record_i = records.index("Michigan")
	#record = records[record_i]
	#print record
	i = 0

	db = MySQLdb.connect(
	    host = constants.HOST_CONST,
	    user = constants.USER_CONST,
	    passwd = constants.PASSWRD_CONST,
	    db = constants.DB_CONST
	)
	cursor = db.cursor()
	for team in teams:

		try:
			#print team
			record = records[i]

			#print record['team']
			#print record


			streak = record['streak']
			#sql
			
			table = ''
			col = ''
			if sport == "NCAAB":
				col = "CB_Record"
			elif sport == "NCAAF":
				col = "CF_Record"
			else:
				col = ''
			col = ''

			if sport == "NCAAB":
				rec = str(record['wins']) + "-" + str(record['losses'])

				#cursor.execute("INSERT INTO NCAA (name, CB_Record, CB_Streak, CF_Record, CF_Streak, CF_PF, CF_PA, CB_PF, CB_PA, CB_PERCENT, CB_LINK) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[team, rec, streak, col, col,col,col,col,col,col,col])

				cursor.execute("UPDATE NCAA SET CB_Record=%s,CB_Streak=%s WHERE name=%s",[rec, streak, team])
			else:

				pa = record['PA']
				pf = record['PF']
				rec = record['rec']

				#cursor.execute("INSERT INTO NCAA (name, CB_Record, CB_Streak, CF_Record, CF_Streak, CF_PF, CF_PA, CB_PF, CB_PA, CB_PERCENT, CB_LINK) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[team, col, col, rec, streak,str(pf),str(pa),col,col,col,col])
				cursor.execute("UPDATE NCAA SET CF_Record=%s,CF_Streak=%s,CF_PA=%s,CF_PF=%s WHERE name=%s",[rec, streak, str(pa), str(pf), team])

			db.commit()
		except:

			record = []
		i += 1
	return

def _main(sport):
	url = ''

	#sport = "NCAAB"
	if sport == "NCAAB":
		url = "http://www.ncaa.com/standings/basketball-men/d1"
	elif sport == "NCAAF":
		url = "http://www.ncaa.com/standings/football/fbs"
	updateRecords(sport, url)


#_main("NCAAF")
_main("NCAAB")