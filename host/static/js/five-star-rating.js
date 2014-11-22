$(".group-stars").on('click', function() {
	checkForLoginBeforeLeavingRating();
});

function renderRatingStars(rating) {
	var myRating = Math.round(parseFloat(rating));
	for (var i = 1; i <= 5; i++) {
		if (i <= myRating)
			{$("#star"+i).attr("class", "jr-ratenode jr-rating");}
		else
			{$("#star"+i).attr("class", "jr-ratenode jr-nomal");}
	};
}

function getRating() {
	var parking_id = getCurrentParkingIdOfOpenedParkingWindow();
	$.ajax({
		url : "/getRating/",
		type : 'GET', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		data : {
			parking_id : parking_id,
		},
		success : function(data) {
			renderRatingStars(data);
			$('.group-stars').start();
		},
		error : function(error) {

			// Log any error.
			console.log("ERROR:", error);

		},
	});

}

function checkForLoginBeforeLeavingRating() {
	$.ajax({
		url : "/checkForLogin/",
		type : 'GET', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		success : function(data) {
			if (data == "Authenticated")
				sendRating();
			else
				$(".signInBox").show();
		},
		error : function(error) {

			// Log any error.
			console.log("ERROR:", error);

		},
	});
}

function sendRating() {
	var parking_id = getCurrentParkingIdOfOpenedParkingWindow();
	var rating = parseInt($(".group-stars").getCurrentRating());
	$.ajax({
		url : "/addRating/",
		type : 'POST', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		data : {
			parking_id : parking_id,
			rating : rating,
		},
		success : function(data) {
			$(".group-stars").hide();
			alert("Благодарим Ви!");
		},
		error : function(error) {

			// Log any error.
			console.log("ERROR:", error);

		},
	});
}

/*
 <span class="group1">
 <div   class="jr-ratenode jr-nomal rating-star"></div>
 <div   class="jr-ratenode jr-nomal rating-star"></div>
 <div   class="jr-ratenode jr-nomal rating-star"></div>
 <div   class="jr-ratenode jr-nomal rating-star"></div>
 <div   class="jr-ratenode jr-nomal rating-star"></div>
 </span>*/