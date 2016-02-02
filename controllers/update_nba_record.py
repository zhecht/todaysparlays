from urllib2 import urlopen
from lxml import etree
import urllib2
import MySQLdb
import constants




def update_nba():

	db = MySQLdb.connect(
		host = constants.HOST_CONST,
		user = constants.USER_CONST,
		passwd = constants.PASSWRD_CONST,
		db = constants.DB_CONST
	)

	cursor = db.cursor()

	url = "https://erikberg.com/nba/standings.xml"

	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	req = urllib2.Request(url, headers=hdr)
	html = urllib2.urlopen(req)
	#html = urllib2.urlopen(url)
	doc = etree.parse(html)
	html.close()


	for team in doc.findall("//team"):

		name = team.find("team-metadata/name").get('last').lower()
		records = team.findall("team-stats/outcome-totals")
		total_events = team.find("team-stats").get("events-played")

		rec = records[0]
		wins = rec.get("wins")
		losses = rec.get("losses")
		streak_type = rec.get("streak-type")
		PF = rec.get("points-scored-for")
		PA = rec.get("points-scored-against")

		PF = float(float(PF) / int(total_events))
		PA = float(float(PA) / int(total_events))

		if streak_type == "loss":
			streak_type = "-"
		else:
			streak_type = "+"

		streak_total = rec.get("streak-total")

		last_10 = records[len(records)-1]
		last_10_wins = last_10.get('wins')
		last_10_losses = last_10.get('losses')


		#cursor.execute("INSERT INTO NBA (name, record, PF, PA, streak, last_10_record, percent, link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[name, wins+"-"+losses, PF, PA, streak_type+streak_total, last_10_wins+"-"+last_10_losses, " ", " "])
		cursor.execute("UPDATE NBA SET record=%s, last_10_record=%s, streak=%s, PF=%s, PA=%s WHERE name=%s",[wins+"-"+losses, last_10_wins+"-"+last_10_losses, streak_type+streak_total, PF, PA, name])
		db.commit()


update_nba()
