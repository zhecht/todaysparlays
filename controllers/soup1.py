import urllib2
import constants
from lxml import etree
from datetime import datetime #python-dateutil
from sql_helper import *
from dateutil import tz
import httplib

def get_time():
	dt = datetime.now()
	return dt.strftime("%I:%M %p")

def get_date():
	dt = datetime.now()
	return dt.strftime("%A, %B %d")

def convert_local(dt):
	from_zone = tz.tzutc()
	to_zone = tz.tzlocal()
	utc = dt.replace(tzinfo=from_zone)

	central = utc.astimezone(to_zone)
	return central

def get_games(sport):

	sporttype = ""
	subtype = ""
	if sport == "NCAAB" or sport == "NBA":
		sporttype = "Basketball"
	else:
		sporttype = "Football"

	if sport == "NCAAF" or sport == "NCAAB":
		subtype = "NCAA"
	else:
		subtype = "NBA"

	url = "http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=" +sporttype+ "&sportsubtype=" +subtype

	if sport == "NFL":
		html = open("/home/zhecht/todaysparlays/static/xml/nfl.xml")
		#html = open("static/xml/nfl.xml")
	elif sport == "NBA":
		html = open("/home/zhecht/todaysparlays/static/xml/nba.xml")
		#html = open("static/xml/nba.xml")
	elif sport == "NCAAB":
		html = open("/home/zhecht/todaysparlays/static/xml/ncaab.xml")
		#html = open("static/xml/ncaab.xml")
	else:
		html = open("/home/zhecht/todaysparlays/static/xml/ncaaf.xml")
		#html = open("static/xml/ncaaf.xml")

	#html = open("static/xml/nba.xml")
	#html = urllib2.urlopen(url)
	doc = etree.parse(html)
	html.close()

	games = []
	counter = 0


	for event in doc.xpath('//event'):
		date = event.find('event_datetimeGMT').text
		teams = event.findall('participants/participant/participant_name')
		away = teams[0].text
		home = teams[1].text

		dt = datetime.strptime(date, "%Y-%m-%d  %H:%M")
		date = convert_local(dt).strftime("%-I:%M %p %-m/%-d")

		periods = event.findall('periods/period')
		#print away
		try:
			period = periods[0]
			spread_away = period.find('spread/spread_visiting').text
			adjust_away = period.find('spread/spread_adjust_visiting').text
			total = period.find('total/total_points')
			adjust_over = period.find('total/over_adjust')
			adjust_under = period.find('total/under_adjust')
			spread_home = period.find('spread/spread_home').text
			adjust_home = period.find('spread/spread_adjust_home').text
		except:
			spread_away = "N/A"
			adjust_away = "N/A"
			total = "N/A"
			adjust_over = "N/A"
			adjust_under = "N/A"
			spread_home = "N/A"
			adjust_home = "N/A"


		if total == None or total == "N/A":
			total = "N/A"
		else:
			total = total.text
		if adjust_over == None or adjust_over == "N/A":
			adjust_over = "N/A"
		else:
			adjust_over = adjust_over.text
		if adjust_under == None or adjust_under == "N/A":
			adjust_under = "N/A"
		else:
			adjust_under = adjust_under.text

		asplit = away.split()
		asplit = asplit[len(asplit)-1].lower()
		hsplit = home.split()
		hsplit = hsplit[len(hsplit)-1].lower()
		if sport == "NBA":

			if asplit == "blazers":
				asplit = "trail blazers"
			elif hsplit == "blazers":
				hsplit = "trail blazers"


			away_stats = getNBAStats(asplit)
			home_stats = getNBAStats(hsplit)

			try:
				stats =  away_stats[0]
			except:
				return games

			away_record = stats[1]
			away_PF = '{0:.5}'.format(stats[2])
			away_PA = '{0:.5}'.format(stats[3])
			away_streak = stats[4]
			away_L10 = stats[5]

			stats =  home_stats[0]
			home_record = stats[1]
			home_PF = '{0:.5}'.format(stats[2])
			home_PA = '{0:.5}'.format(stats[3])
			home_streak = stats[4]
			home_L10 = stats[5]

		elif sport == "NFL":
			away_stats = getNFLStats(asplit)
			home_stats = getNFLStats(hsplit)

			away_streak = None
			home_streak = None
			home_L10 = None
			away_L10 = None

			date = convert_local(dt).strftime("%a %I:%M")
			try:
				stats =  away_stats[0]
			except:
				return games

			away_record = stats[1]
			away_PF = '{0:.5}'.format(stats[2])
			away_PA = '{0:.5}'.format(stats[3])

			stats =  home_stats[0]
			home_record = stats[1]
			home_PF = '{0:.5}'.format(stats[2])
			home_PA = '{0:.5}'.format(stats[3])

		else:

			away_name = get_NCAA_DB_Name(away)
			home_name = get_NCAA_DB_Name(home)

			away_stats = getNCAAStats(away_name, sport)
			home_stats = getNCAAStats(home_name, sport)

			try:
				stats =  away_stats[0]
				away_record = stats[0]
				away_streak = stats[1]
				
			except:
				away_record = ''
				away_streak = ''

			try:
				stats1 = home_stats[0]
				home_record = stats1[0]				
				home_streak = stats1[1]
				
			except:
				home_record = ''
				home_streak = ''
			
			away_stats = get_public(away_name, "NCAAB")
			home_stats = get_public(home_name, "NCAAB")
			try:
				stats =  away_stats[0]
				away_percent = stats[0]
				away_link = stats[1]
			except:
				away_percent = ''
				away_link = ''
			try:
				stats1 = home_stats[0]
				home_percent = stats1[0]
				home_link = stats1[1]
			except:
				home_percent = ''

		#print away_record
		if sport == "NBA" or sport == "NFL":
			#print away_record
			#print home_record
			games.append({'index': counter, 'away': away, 'home': home, 'spread_away': spread_away, 'adjust_away': adjust_away, 'spread_home': spread_home, 'adjust_home': adjust_home, 'date': date, 'total': total, 'adjust_over': adjust_over, 'adjust_under': adjust_under, 'record_home': home_record, 'record_away': away_record, 'streak_away': away_streak, 'streak_home': home_streak, 'away_PF': away_PF, 'away_PA': away_PA, 'away_L10': away_L10, 'home_PF': home_PF, 'home_PA': home_PA, 'home_L10': home_L10})
		else:
			games.append({'index': counter, 'away': away, 'home': home, 'spread_away': spread_away, 'adjust_away': adjust_away, 'spread_home': spread_home, 'adjust_home': adjust_home, 'date': date, 'total': total, 'adjust_over': adjust_over, 'adjust_under': adjust_under, 'record_home': home_record, 'record_away': away_record, 'streak_away': away_streak, 'streak_home': home_streak, 'percent_away': away_percent, 'percent_home': home_percent, 'link': away_link})
		counter += 1

	return games













