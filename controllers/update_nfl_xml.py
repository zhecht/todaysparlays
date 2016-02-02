import urllib2

def update_lines():

	url = "http://xml.pinnaclesports.com/pinnaclefeed.aspx?sporttype=Basketball&sportsubtype=NCAA"
	html = urllib2.urlopen(url).read()

	print html

update_lines()
