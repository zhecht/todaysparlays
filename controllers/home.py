from flask import *
from soup1 import *
#from update_record import *

home = Blueprint('home', __name__, template_folder='views')


@home.route('/', methods=["GET"])
def home_route():

	sport = request.args.get('s')

	sub =""
	home =""

	if sport == None:
		sport = "NCAAB"
	

	games = get_games(sport)
	#games = []

	#reddit = get_reddit(curr_sub)
	#weather = get_weather("Merrick")
	#weather = []

	#location = "Ann Arbor"
	
	date = get_date()
	time = get_time()

	return render_template("home.html", games=games, date=date, time=time, sport=sport)
