from bs4 import BeautifulSoup
import urllib2
import constants
import MySQLdb

db = MySQLdb.connect(
    host = constants.HOST_CONST,
    user = constants.USER_CONST,
    passwd = constants.PASSWRD_CONST,
    db = constants.DB_CONST
    )

cursor = db.cursor()


def get_ppg():
	url = "http://fantasydata.com/nfl-stats/nfl-team-stats.aspx"
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	html = urllib2.urlopen(req).read()

	#html = open("nfl.html").read()
	soup = BeautifulSoup(html, "lxml")

	grid = soup.find('table', id='StatsGrid')


	count = 0
	
	for tr in grid.find_all("tr"):

		if count != 0:

			i = 0
			tname = ''
			ppg  = ''
			total_games = 0
			for td in tr.find_all("td", limit=4):
				if i == 1:
					name = td.text
					name = name.split(" ")[-1]
					tname = name.lower()
				elif i == 2:
					total_games = int(td.text)
				elif i == 3:
					ppg = td.text

				i += 1
			
			cursor.execute("SELECT PF,PA FROM NFL WHERE name=%s",[tname])
			res = cursor.fetchall()[0]
			
			pf = float(float(res[0]) / float(total_games))
			pa = float(float(res[1]) / float(total_games))

			cursor.execute("UPDATE NFL SET PF=%s,PA=%s WHERE name=%s", [pf, pa, tname])
			db.commit()
		count += 1

def get_records():

	url = "http://fantasydata.com/nfl-stats/standings.aspx"
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	html = urllib2.urlopen(req).read()

	#html = open("nfl.html").read()
	soup = BeautifulSoup(html, "lxml")

	tables = soup.find_all('table', class_='standings')


	for table in tables:

		i = 0
		team_name = ''
		wins = ''
		losses = ''
		PF = ''
		PA = ''
		total_pts = ''
		#print table.find_all("td")
		for nfl_data in table.find_all("td"):
			data = nfl_data.text

			if i == 0: #name
				name = data
				name_s = name.split(" ")
				team_name = name_s[-1].lower()
			elif i == 1: #wins
				wins = data
			elif i == 2:
				losses = data
			elif i == 5:
				PF = int(data)
			elif i == 6:
				PA = int(data)
			elif i == 7:
				total_pts = int(data)

			i += 1

			if i == 11:
				#print team_name
				#print PF
				#print PA
				#print total_pts
				record = wins +"-"+ losses
				cursor.execute("UPDATE NFL SET record=%s, PF=%s, PA=%s WHERE name=%s",[record,PF,PA,team_name])
				db.commit()
				i = 0
		

#cron
get_records()	
get_ppg()

