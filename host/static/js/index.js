function getLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(showPosition, errorCall, {
			enableHighAccuracy : true,
		});
	} else {
		alert("The browser cannot geocode your position!");
	}
}function errorCall() {
	alert("The browser cannot geocode your position!");
}function showPosition(position) {
	$('.lat').val(position.coords.latitude);
	$('.lng').val(position.coords.longitude);
	//alert(position.coords.latitude + " " + position.coords.longitude);
	document.getElementsByClassName('submitButton')[0].click();
}function closeSubscribe() {
	$('.subscribeBox').hide();
	//$('.subscribeButton').hide();
	$('.on-landing').show();
	shouldOpen = true;
}var shouldOpen = true;
function showBookingMsg(book) {
	//alert($('.subscribeBox')[0].length);
	if (shouldOpen) {
		shouldOpen = false;
		$('.on-landing').hide();
		renderInfoMsg(book);
		$('.subscribeBox').show();
		//$('.subscribeButton').show();
	}
}function renderSubscribeMsg() {
	$('.msg').html("");
	if ("{{msg}}" == "thanks")
		var msg = "Благодаря Ви!";	
else if ("{{msg}}" == "notValid")
		var msg = "Въвели сте невалиден адрес!";	
else if ("{{msg}}" == "existing")
		var msg = "Емейлът вече съществува!";
	$('.msg').html(msg);
}//<input type='text' placeholder='Име и фамилия' class='sub-name form-control'/>
function submitViewer() {
	//$('.sub-button').trigger();
	document.getElementsByClassName('sub-button')[0].click();
}function renderInfoMsg(book) {
	$('.msg').html("");
	if (book)
		var msg = "Тази функционалност предстои да бъде активирана. За да Ви уведомим, когато е готова, както и друга полезна информация, моля оставете име и е-мейл.";	
else
		var msg = "";
	$('.msg').html(msg);
}function renderNumberOfHelped(number) {
	var currentNumber = $('.customers').html();
	currentNumber = currentNumber + number.split('-')[1];
	$('.customers').html(currentNumber);
	setTimeout(function() {
		$('.customers').html(number.split('-')[0]);
	}, 1000);
	/*
	 var currentNumber = $('.customers').html();
	 currentNumber = currentNumber + " +1 ";
	 $('.customers').html(currentNumber);
	 setTimeout(function() {
	 $('.customers').html(number);
	 }, 1000);*/
}function setFocus() {
	$('#addressInput').focus();
}$('#location').bind("keyup keypress", function(e) {
	var code = e.keyCode || e.which;
	if (code == 13) {
		e.preventDefault();
		return false;
	}
});
//hrome onenter event
$('#addressInput').keydown(function(event) {
	var keypressed = event.keyCode || event.which;
	if (keypressed == 13) {
		getCoordinationsByGeocoding();
	}
});