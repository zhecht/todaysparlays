import urllib2
from bs4 import BeautifulSoup
import constants
import MySQLdb
#url = "http://www.thespread.com/nba-basketball-public-betting-chart"
#req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
#html = urllib2.urlopen(req).read()
#nba_soup = BeautifulSoup(html, "lxml")

db = MySQLdb.connect(
    host = constants.HOST_CONST,
    user = constants.USER_CONST,
    passwd = constants.PASSWRD_CONST,
    db = constants.DB_CONST
    )

def make_cursor():
	
	return db.cursor()

def check_name(name, sport):

	if name == "nebraska omaha":
		return "nebraska-omaha"
	elif name == "st. joseph's":
		return "st. joseph's (pa)"

	if sport == "NBA":
		hold = name.split(" ")[-1]
		if hold.lower() == "blazers":
			name = "trail blazers"
		else:
			name = hold.lower()
	return name

def update(url, sport):

	#url = "http://www.oddsshark.com/ncaab/consensus-picks"
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	html = urllib2.urlopen(req).read()
	ncaab_soup = BeautifulSoup(html, "lxml")

	table = ncaab_soup.find('table', class_='consensus-table')

	i = 0
	team_c = 0
	cursor = make_cursor()
	percent_v = '%'
	percent_h = '%'
	name_v = ''
	name_h = ''
	link = ''
	for tr in table.find_all('tr'):
		#print tr
		if i != 0:
			
			if team_c % 3 == 0: #away
				percent = tr.find("td", class_="consensus").text
				percent_v = int(percent[:-1])
				name = tr.find("a", class_="name-long").text
				name_v = check_name(name.lower(), sport)

			elif team_c % 3 == 1: #home
				
				percent_h = 100 - percent_v
				name = tr.find("a", class_="name-long").text
				name_h = check_name(name.lower(), sport)

			else: #link
				link = tr.find("a").get("href")

				if sport == "NCAAB":
					cursor.execute("UPDATE NCAA SET CB_PERCENT=%s,CB_LINK=%s WHERE name=%s", [str(percent_v) + '%', link, name_v])
					cursor.execute("UPDATE NCAA SET CB_PERCENT=%s,CB_LINK=%s WHERE name=%s", [str(percent_h) + '%', link, name_h])
				elif sport == "NBA":
					cursor.execute("UPDATE NBA SET percent=%s,link=%s WHERE name=%s", [str(percent_v) + '%', link, name_v])
					cursor.execute("UPDATE NBA SET percent=%s,link=%s WHERE name=%s", [str(percent_h) + '%', link, name_h])
				
				#return

			team_c += 1
		i += 1
	
	db.commit()

update("http://www.oddsshark.com/ncaab/consensus-picks", "NCAAB")
update("http://www.oddsshark.com/nba/consensus-picks", "NBA")