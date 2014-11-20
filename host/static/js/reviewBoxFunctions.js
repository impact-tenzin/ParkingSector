/*
 <li class='left clearfix'>
 <span class='chat-img pull-left'> <img src='https://graph.facebook.com/Authenticated/picture'; alt='User Avatar' class='img-circle' /> </span>
 <div class='chat-body clearfix'>
 <div class='header'>
 <strong class='primary-font'>Пешо Марков</strong><small class='pull-right text-muted'> 15.03.2014 <span class='glyphicon glyphicon-time'></span>12:45</small>
 </div>
 <p>
 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum ornare
 dolor, quis ullamcorper ligula sodales.
 </p>
 </div>
 </li>
 */

function getReviews() {
	
	//var parking_id = parseInt($('#window-selected-id').attr('class'));
	var parking_id = idOfOpenParkingWindow;
	$('#reviewBox').html("");
	$(".rateAndReviewBox").show();

	$.ajax({
		url : '/getParkingReviews/',
		type : 'GET', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		data:{
			parking_id : parking_id
		},
		success : function(data) {
			parseDataAndRenderOnUI(data);
		},
		error : function(error) {
			// Log any error.
			console.log('ERROR:', error);
		},
	});

}

function closeRateAndReviewBox()
{
	$('.rateAndReviewBox').hide();
}

function parseDataAndRenderOnUI(data) {
	parkingReviews = [];
	var reviews = data.filter(function(item) {
		return item.model == 'user.parkingreview';
	});

	parseReviews(reviews);
	renderOnUI();
}

function parseReviews(reviews) {
	for (var i = 0, len = reviews.length; i < len; i++) {
		//var parking = ajaxParkings[i].split('&');
		var currentReview = new Object();
		currentReview.id = parseInt(reviews[i].pk);
		currentReview.parking_id = reviews[i].fields['parking_id'];
		currentReview.fb_id = reviews[i].fields['fb_id'];
		currentReview.username = reviews[i].fields['username'];
		currentReview.date = reviews[i].fields['date'];
		currentReview.review = reviews[i].fields['review'];
		parkingReviews.push(currentReview);
	};
}

function renderOnUI() {
	for (var i=parkingReviews.length-1; i >= 0; i--) {
		li = document.createElement('li');
		li.className = 'left clearfix';
		li.innerHTML = " <span class='chat-img pull-left'> "+getImage(parkingReviews[i].fb_id)+" </span>"+
						" <div class='chat-body clearfix'>"+
						 "<div class='header'>"+
						 "<strong class='primary-font'>"+parkingReviews[i].username+"</strong><small class='pull-right text-muted'> "+parkingReviews[i].date.split(" ")[0]+" <span class='glyphicon glyphicon-time'></span>"+parkingReviews[i].date.split(" ")[1]+"</small>"+
						" </div>"+
						" <p>"+
						 parkingReviews[i].review
						+" </p>"+
						 "</div>";
		document.getElementById('reviewBox').appendChild(li);
	};
}

function getImage(fb_id)
{
	if (fb_id.length > 0)
		return "<img src='https://graph.facebook.com/"+fb_id+"/picture'; alt='User Avatar' class='img-circle' />";
	else
		return "<img src='/static/imgs/default.jpg'; width='50' height='50' alt='User Avatar' class='img-circle' />";
}

function getCurrentDate2() {
	var date = new Date();
	var dateString = date.getDate() + "." + appendZero(date.getMonth()) + (date.getMonth() + 1) + "." + date.getFullYear() + " " + date.getHours() + ":" + date.getMinutes();
	return dateString;
}

function addReview()
{
	if ($(".reviewInput").val().trim() == "") return;
	var parking_id = parseInt($('#window-selected-id').attr('class'));
	var date = getCurrentDate2()
	var review = $(".reviewInput").val();
	
	$.ajax({
		url : '/addParkingReview/',
		type : 'POST', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		data:{
			parking_id : parking_id,
			review : review,
			date : date,
		},
		success : function(data) {
			$('#reviewBox').html("");
			$(".reviewInput").val("");
			getReviews();
		},
		error : function(error) {
			// Log any error.
			console.log('ERROR:', error);
		},
	});
}

function checkForLoginBeforeLeavingReview() {
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
						addReview();
					else
						$(".signInBox").show();
				},
				error : function(error) {

					// Log any error.
					console.log("ERROR:", error);

				},
			});
		}