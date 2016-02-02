import urllib2
from lxml import etree

def update_lines():

	url = "http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=Basketball&sportsubtype=NBA"
	html = urllib2.urlopen(url)
	doc = etree.parse(html)
	html.close()
	out = open("/home/zhecht/todaysparlays/static/xml/nba.xml", "w")
	out.truncate()
	out.close()
	doc.write("/home/zhecht/todaysparlays/static/xml/nba.xml")



update_lines()
