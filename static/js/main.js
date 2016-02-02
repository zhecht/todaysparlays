
function changeop() {
	'use strict';
	$('#hiddenInput').val("signup");
	$('#menu').submit();
}


function showRedditSearch() {
	'use strict';
	$('#searchRedditForm').fadeIn(400);
}


function update_weather(id, time) {
	'use strict';

	var weather = "",
		time_split = time.split(" "),
		ampm = time_split[1],
		hour = parseInt(time_split[0].split(":")[0]);

	//alert(time_split);
	
	if (id >= 300 && id < 522) {
		//rain
		weather = "rainy";
	}
	else if (id >= 600 && id < 623) {
		weather = "snowy";
	}
	else if ((ampm === "AM" && hour <= 6) || (ampm == "PM" && hour > 7)) {
		weather = "starry";
	}
	else if (id === 960 || id === 522 || id === 531 || (id > 199 && id < 233)) {
		weather = "stormy";
	}
	else if ((id > 800 && id < 805) || id === 701 || id === 721 || id === 741) {
		//clouds,mist,haze,fog
		weather = "cloudy";
	}
	else {
		weather = "sunny";
	}
	var prev = $('.weather div').attr('class');
	$('.weather div').removeClass(prev).addClass(weather);

}