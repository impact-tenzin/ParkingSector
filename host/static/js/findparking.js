function setFocus() {
	$(".searchBar").focus();
}

// get address latitude and longitude or precalculates the parking prices
function getCoords(autocomplete) {
	/*
	 if (!checkForProperTimeDuration()) {
	 alert("Р§Р°СЃСЉС‚ РЅР° РёР·Р»РёР·Р°РЅРµ РЅРµ РјРѕР¶Рµ РґР° РїСЂРµРґС…РѕР¶РґР° С‡Р°СЃР° РЅР° РІР»РёР·Р°РЅРµ, Р° РїСЂРµСЃС‚РѕСЏС‚ Рµ РјРёРЅРёРјСѓРј Р·Р° 1 С‡Р°СЃ!");
	 } else {*/

	var place = autocomplete.getPlace();
	if (!place.geometry) {
		return;
	}
	var lat = place.geometry.location.lat();
	var lng = place.geometry.location.lng();
	ajaxCall(lat, lng);
	markerCenter.setMap(null);
	markerCenter = new google.maps.Marker({
		map : map,
		draggable : true,
		position : new google.maps.LatLng(lat, lng)
	});
	map.setCenter(new google.maps.LatLng(lat, lng));

	google.maps.event.addListener(markerCenter, 'dragend', function() {
		ajaxCall(markerCenter.position.lat(), markerCenter.position.lng());
		map.setCenter(new google.maps.LatLng(markerCenter.position.lat(), markerCenter.position.lng()));
	});
	/*
	address = $('.searchBar').val();

	geocoder.geocode({
	address : address
	}, function(results, status) {
	if (status == google.maps.GeocoderStatus.OK) {
	var lat = results[0].geometry.location.lat();
	var lng = results[0].geometry.location.lng();
	ajaxCall(lat, lng);
	markerCenter.setMap(null);
	markerCenter = new google.maps.Marker({
	map : map,
	draggable : true,
	position : new google.maps.LatLng(lat, lng)
	});
	map.setCenter(new google.maps.LatLng(lat, lng));

	google.maps.event.addListener(markerCenter, 'dragend', function() {
	ajaxCall(markerCenter.position.lat(), markerCenter.position.lng());
	map.setCenter(new google.maps.LatLng(markerCenter.position.lat(), markerCenter.position.lng()));
	});
	}
	});*/

	//}
}

//remove last else and previous else-if -> only else when filling all info
function triggerWindowForChosenParking(lat, lng) {
	for (var i = 0, len = parkings.length; i < len; i++) {
		if (lat == parkings[i].lat) {
			if (markers[i].icon == "/static/imgs/parkingPointer.png" || markers[i].icon == "/static/imgs/parkingPointerBlurred.png") {
				showMarkerWindow(parkings[i], markers[i]);
				break;
			} else if (markers[i].icon == "/static/imgs/parkingPointerBlurredNA.png") {
				showMarkerWindowNA(parkings[i], markers[i]);
				break;
			} else {
				showMarkerWindowNoInfo(parkings[i], markers[i]);
				break;
			}
		}
	};
}

// get the length of parkings that are active
function getParkingsLength() {
	var number = 0;
	for (var i = 0, len = markers.length; i < len; i++) {
		if (markers[i].icon == "/static/imgs/parkingPointer.png")
			number++;
	}
	return number;
}

// renders parking length
function displayNumberOfFoundParkings(parkings) {
	document.getElementById('numberOfParkings').innerHTML = '';
	var length = getParkingsLength();
	if (length == 1)
		var number = "<div>" + "<span style='color:rgb(27,162,217);font-size:18px'>" + length + "</span>" + " паркинг" + "</div>";
	else
		var number = "<div>" + "<span style='color:rgb(27,162,217);font-size:18px'>" + length + "</span>" + " паркинга" + "</div>";
	document.getElementById('numberOfParkings').innerHTML = number;
}

// returns payment method on given id and methods list
function getPaymentMethod(methodId, methods) {
	for (var i = 0, len = methods.length; i < len; i++) {
		if (methods[i].id == methodId)
			return methods[i];
	};
}

// checks if parking works during the selected time frame
/*
function checkIfParkingWorks(parking) {
var dateFrom = $('#fromDate').val().split(' ');
var hourFrom = parseInt(dateFrom[1].split(':')[0]);
var periodFrom = parseInt(dateFrom[1].split(':')[1]);

var dateTo = $('#toDate').val().split(' ');
var hourTo = parseInt(dateTo[1].split(':')[0]);
var periodTo = parseInt(dateTo[1].split(':')[1]);

var arrival = hourFrom + (periodFrom / 100);
var departure = hourTo + (periodTo / 100);

if (arrival >= (parseFloat(parking.workFrom)).toFixed(2) && arrival <= (parseFloat(parking.workTo)).toFixed(2) && departure <= (parseFloat(parking.workTo)).toFixed(2) && departure >= (parseFloat(parking.workFrom)).toFixed(2))
return true;
return false;

}*/

// create marker on map and there are two types, one for active parkings and one for those that do not work
// during the selected hours
function createMarker(parking, i) {
	if (parking.pricePerHour != 0) {
		//if (checkIfParkingWorks(parking)) {
		//calcPrice(parking);
		var marker = new MarkerWithLabel({
			position : new google.maps.LatLng(parseFloat(parking.lat), parseFloat(parking.lng)),
			draggable : false,
			map : map,
			labelVisible : true,
			icon : "/static/imgs/parkingPointer.png",
			//labelContent : "<p>" + parking.price + " " + "<span class='spanlv'>лв</span>" + "</p>",
			labelAnchor : new google.maps.Point(30, 33),
			labelClass : "labels", // the CSS class for the label
		});
		marker.lat = parking.lat;
		addClickListener(marker, i, parking);
		markers.push(marker);
		/*
		 } else {
		 var marker = new MarkerWithLabel({
		 position : new google.maps.LatLng(parseFloat(parking.lat), parseFloat(parking.lng)),
		 draggable : false,
		 map : map,
		 labelVisible : true,
		 icon : "/static/imgs/parkingPointerBlurredNA.png",
		 //labelContent : "<p>N/A</p>",
		 labelAnchor : new google.maps.Point(30, 33),
		 labelClass : "labels", // the CSS class for the label
		 });
		 marker.lat = parking.lat;
		 addClickListener(marker, i, parking);
		 markers.push(marker);
		 }*/

	} else {
		var marker = new MarkerWithLabel({
			position : new google.maps.LatLng(parseFloat(parking.lat), parseFloat(parking.lng)),
			draggable : false,
			map : map,
			labelVisible : true,
			icon : "/static/imgs/parkingPointerNoInfo.png",
			//labelContent : "",
			labelAnchor : new google.maps.Point(30, 33),
			labelClass : "labels", // the CSS class for the label
		});
		marker.lat = parking.lat;
		addClickListener(marker, i, parking);
		markers.push(marker);
	}
}

// add proper onclick events depending on active or nonactive parking
function addClickListener(marker, i, parking) {
	if (marker.icon == "/static/imgs/parkingPointer.png" || marker.icon == "/static/imgs/parkingPointerBlurred.png")
		handlers[i] = google.maps.event.addListener(marker, 'click', function() {
			showMarkerWindow(parking, marker);
		});
	else if (marker.icon == "/static/imgs/parkingPointerBlurredNA.png")
		handlers[i] = google.maps.event.addListener(marker, 'click', function() {
			showMarkerWindowNA(parking, marker);
		});
	else
		handlers[i] = google.maps.event.addListener(marker, 'click', function() {
			showMarkerWindowNoInfo(parking, marker);
		});
}

// calculating price for the selected time frame
/*
function calcPrice(parking) {
var dateFrom = $('#fromDate').val().split(' ');
var dayFrom = parseInt(dateFrom[0].split('.')[0]);
var monthFrom = parseInt(dateFrom[0].split('.')[1]) - 1;
var yearFrom = parseInt(dateFrom[0].split('.')[2]);
var hourFrom = parseInt(dateFrom[1].split(':')[0]);
var periodFrom = parseInt(dateFrom[1].split(':')[1]);

var dateTo = $('#toDate').val().split(' ');
var dayTo = parseInt(dateTo[0].split('.')[0]);
var monthTo = parseInt(dateTo[0].split('.')[1]) - 1;
var yearTo = parseInt(dateTo[0].split('.')[2]);
var hourTo = parseInt(dateTo[1].split(':')[0]);
var periodTo = parseInt(dateTo[1].split(':')[1]);

var starttime = (new Date(yearFrom, monthFrom, dayFrom, hourFrom, periodFrom, 0)).getTime();
var endtime = (new Date(yearTo, monthTo, dayTo, hourTo, periodTo, 0)).getTime();

var time = parseInt(((endtime - starttime ) / 3600000));
if (Math.abs(((endtime / 3600000) - (starttime / 3600000))) % 1 != 0)
time++;
parking.price = (parking.pricePerHour * time).toFixed(1);
}*/

// used to precalculate prices when there is new time frame on the same address
/*
function preCalculatePrices() {
clearLocations();
for (var i = 0, len = parkings.length; i < len; i++) {
createMarker(parkings[i], i);
};
displayFoundParkings(parkings);
displayNumberOfFoundParkings(parkings);
}*/

// add proper values to latitude to fit the map depending on the zoom level
function getDistance(zoom) {
	switch (zoom) {
		case 5:
			return 1.5;
		case 6:
			return 0.9;
		case 7:
			return 0.5;
		case 8:
			return 0.3;
		case 9:
			return 0.2;
		case 10:
			return 0.1;
		case 11:
			return 0.05;
		case 12:
			return 0.02;
		case 13:
			return 0.01;
		case 14:
			return 0.006;
		case 15:
			return 0.0026;
		case 16:
			return 0.0015;
		case 17:
			return 0.0007;
		case 18:
			return 0.00032;
		case 19:
			return 0.00018;
		case 20:
			return 0.00009;
		case 21:
			return 0.000045;
	}
}

function hasCapacity(capacity) {
	if (capacity > 0)
		return capacity;
	else
		return "--";
}

var coloredParkingId;
function closeBox() {
	ib.close();
	$("#" + coloredParkingId).parent().attr('class', 'displayedParking non-highlighted');
}

function highlightParking(parking) {
	var id = parking.id;
	if (coloredParkingId != undefined)
		$("#" + coloredParkingId).parent().attr('class', 'displayedParking non-highlighted');
	var parkingList = document.getElementsByClassName('id-parking');
	for (var i = 0; i < parkingList.length; i++) {
		if (parkingList[i].id == id) {
			$("#" + id).parent().attr('class', "displayedParking highlighted");
			coloredParkingId = id;
			/*
			$('.currentParkings').animate({
			scrollLeft : $("#" + id).parent().offset().left
			}, 2000);*/

			/*
			$('.currentParkings').animate({
			scrollLeft : $("#" + id).parent().offset().left - ($(window).width() - $("#" + id).parent().outerWidth(true) ) / 2
			}, 200);*/
			//centerHighlightedEl(id);
			//alert(id);
			//alert($(".currentParkings").scrollLeft());
			break;
		}
	};
}

function centerHighlightedEl(id) {
	var viewportWidth = jQuery(window).width(), viewportHeight = jQuery(window).height(), $foo = jQuery('#' + id).parent(), elWidth = $foo.width(), elHeight = $foo.height(), elOffset = $foo.offset();
	// jQuery(window)
	$('.currentParkings')
	//.scrollTop(elOffset.top + (elHeight/2) - (viewportHeight/2))
	.scrollLeft(elOffset.left + (elWidth / 2) - (viewportWidth / 2));
}

// information window for active parkings that is shown on clicking a marker
//<span id='displayedPercentage'>" + "--" + "</span> needs api + formula to calculate percentage
function showMarkerWindow(parking, marker) {
	map.panTo(new google.maps.LatLng(parking.lat, parking.lng));
	highlightParking(parking);
	var html = "<div class='infoWindow'>" + "<span class='glyphicon glyphicon-remove closeX' onclick='closeBox();'></span>" + "<div class='win-address'>" + parking.address + "</div>"/* +   "<div class='win-price'><span>" + parking.pricePerHour + " лв/час</span></div>"*/ + "<div class='win-distance'><span class='win-info'>Разстояние:</span><div class='parameters'>" + distToMeters(parking.distance) + "</div></div>" + "<div class='win-time'><span class='win-info'>Работно време:</span><div class='parameters'>" + parking.workFrom + " - " + parking.workTo + "</div></div>" + "<span class='win-info'>Ценоразпис:</span><br><table class='prices'><tr><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th></tr><tr><td>1</td><td>1</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>1</td><td>1</td><td>1</td><td>1</td></tr></table>" + "<div class='win-book' onclick='bookingReqeust();'>Запази място</div>" + "<div id='window-selected-id' class=" + "'" + parking.id + "'" + "hidden></div>" + "</div>";
	var myOptions = {
		content : html,
		disableAutoPan : false,
		maxWidth : 0,
		pixelOffset : new google.maps.Size(-140, 0),
		zIndex : null,
		boxStyle : {
			height : "0px",
			width : "0px",
		},
		closeBoxURL : "",
		infoBoxClearance : new google.maps.Size(1, 1),
		isHidden : false,
		pane : "floatPane",
		enableEventPropagation : false
	};
	ib.setOptions(myOptions);
	ib.open(map, marker);
}

// information window for nonactive parkings that is shown on clicking a marker
function showMarkerWindowNA(parking, marker) {
	map.panTo(new google.maps.LatLng(parking.lat, parking.lng));
	var html = "<div class='infoWindow'>" + "<span class='closeX' onclick='closeBox();'></span>" + "<div class='win-address'>Паркингът не работи в момента.</div>";
	var myOptions = {
		content : html,
		disableAutoPan : false,
		maxWidth : 0,
		pixelOffset : new google.maps.Size(-140, 0),
		zIndex : null,
		boxStyle : {
			height : "0px",
			width : "0px",
		},
		closeBoxMargin : "-295px -347px 2px 2px",
		closeBoxURL : "/static/imgs/close.png",
		infoBoxClearance : new google.maps.Size(1, 1),
		isHidden : false,
		pane : "floatPane",
		enableEventPropagation : false
	};
	ib.setOptions(myOptions);
	ib.open(map, marker);
}

function distToMeters(distance) {
	if (distance > 0.5)
		return (Math.round(distance * 10) / 10).toFixed(1) + " км";
	else
		return (distance).toFixed(3) * 1000 + " метра";
}

// remove after filling info
function showMarkerWindowNoInfo(parking, marker) {
	map.panTo(new google.maps.LatLng(parking.lat, parking.lng));
	var html = "<div class='infoWindow'>" + "<span class='glyphicon glyphicon-remove closeX' onclick='closeBox();'></span>" + "<div class='win-address'>Предстои да добавим информация за паркинга.</div>";
	var myOptions = {
		content : html,
		disableAutoPan : false,
		maxWidth : 0,
		pixelOffset : new google.maps.Size(-140, 0),
		zIndex : null,
		boxStyle : {
			height : "0px",
			width : "0px",
		},
		closeBoxURL : "",
		infoBoxClearance : new google.maps.Size(1, 1),
		isHidden : false,
		pane : "floatPane",
		enableEventPropagation : false
	};
	ib.setOptions(myOptions);
	ib.open(map, marker);
}

/*
$('#location').bind("keyup keypress", function(e) {
var code = e.keyCode || e.which;
if (code == 13) {
e.preventDefault();
return false;
}
});*/
//hrome onenter event
/*
 $('.searchBar').keydown(function(event) {
 var keypressed = event.keyCode || event.which;
 if (keypressed == 13) {
 getCoords();
 }
 });*/

$(".close-parkingsBar").click(function() {
	$(".displayedParkingsBar").animate({
		'height' : 0
	}, 450);
	$(".close-parkingsBar").hide();
	$(".open-parkingsBar").show();
});
$(".open-parkingsBar").click(function() {
	$(".displayedParkingsBar").animate({
		'height' : 137
	}, 450);
	$(".open-parkingsBar").hide();
	setTimeout(function() {
		$(".close-parkingsBar").show();
	}, 450);
});

function bookingReqeust() {
	$.ajax({
		url : "/bookParkingSpot/",
		type : 'GET', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		//dataType : 'json',
		success : function(data) {
			if (data == "Not authenticated")
				bookingMsg();
			else
				preConfirmBooking(data);
		},
		error : function(error) {

			// Log any error.
			console.log("ERROR:", error);

		},
	});
}

function preConfirmBooking(data) {
	$('.confirmBox').show();
	$("#license").html("");
	if (data.length > 0) {
		for (var i = 0; i < data.length; i++) {
			console.log(i);
			$("#license").append("<option value=" + (i + 1) + ">" + data[i].fields['licence_plate'] + "</option>");
		};
	}
}

function bookingMsg() {
	$('.signInBox').show();

	//var idOfParkingClicked = getParkingId(address);
	markBooking(idOfParkingClicked);
}

/*function getParkingId(address) {
 for (var i = 0; i < parkings.length; i++) {
 if (parkings[i].address == address) {
 return parkings[i].id;
 break;
 }
 };
 }*/

function closeSignIn() {
	$('.signInBox').hide();
	$('.msg').html("");
}

function closeConfirm() {
	$('.confirmBox').hide();
	$('.msg-confirm').html("");
}

$(function() {
	$(".close-filters").click(function() {
		closeFilters();
	});
});

function closeFilters() {
	var el = $('.searchBarAndFilters').height();
	if (el > 10) {
		$(".searchBarAndFilters").animate({
			'height' : 10
		}, 350);
		document.getElementsByClassName('searchBarAndFilters-wrapper')[0].style.visibility = 'hidden';
		$('.open-filters').show();
		$('.filters-label').show();
	}
}

$(function() {
	$(".open-filters").click(function() {
		var el = $('.searchBarAndFilters').height();
		if (el < 259) {
			$(".searchBarAndFilters").animate({
				'height' : 280
			}, 350);
			$('.searchBarAndFilters-wrapper').show();
			document.getElementsByClassName('searchBarAndFilters-wrapper')[0].style.visibility = 'visible';
			$('.open-filters').hide();
			$('.filters-label').hide();
		}
	});
});

$(function() {
	$(".filters-label").click(function() {
		var el = $('.searchBarAndFilters').height();
		if (el < 259) {
			$(".searchBarAndFilters").animate({
				'height' : 280
			}, 350);
			$('.searchBarAndFilters-wrapper').show();
			document.getElementsByClassName('searchBarAndFilters-wrapper')[0].style.visibility = 'visible';
			$('.open-filters').hide();
			$('.filters-label').hide();
		}
	});
});

function roundMinutes(minutes) {
	for (var i = 1; i <= 16; i++) {
		if (minutes == 15 || minutes == 30 || minutes == 45)
			return minutes;
		if (minutes == 60)
			return '00';
		minutes += 1;
	};
}

function appendZero(month) {
	if (month < 9)
		return '0';
	return;
}

function getCurrentDate(isToHour) {
	var date = new Date();
	if (roundMinutes(date.getMinutes()) == '00')
		date.setHours(date.getHours() + 1);
	if (isToHour)
		date.setHours(date.getHours() + 1);
	var dateString = date.getDate() + "." + appendZero(date.getMonth()) + (date.getMonth() + 1) + "." + date.getFullYear() + " " + date.getHours() + ":" + roundMinutes(date.getMinutes());
	return dateString;
}

/*
function loadDatePickers() {
$(function() {
$('#fromDate').datetimepicker({
format : 'd.m.Y H:i',
value : getCurrentDate(false),
dayOfWeekStart : 1,
step : 15,
});
$('#toDate').datetimepicker({
format : 'd.m.Y H:i',
value : getCurrentDate(true),
onClose : function() {
if (!checkForProperTimeDuration())
alert("Р§Р°СЃСЉС‚ РЅР° РёР·Р»РёР·Р°РЅРµ РЅРµ РјРѕР¶Рµ РґР° РїСЂРµРґС…РѕР¶РґР° С‡Р°СЃР° РЅР° РІР»РёР·Р°РЅРµ, Р° РїСЂРµСЃС‚РѕСЏС‚ Рµ РјРёРЅРёРјСѓРј Р·Р° 1 С‡Р°СЃ!");
},
dayOfWeekStart : 1,
step : 15,
});
});
}*/

// calculates the distance between two points
function distance(latAddress, lngAddress, lat, lng) {
	Math.radians = function(degrees) {
		return degrees * Math.PI / 180;
	};
	var R = 6371;
	// Radius of the earth in km
	var dLat = Math.radians(lat - latAddress);
	// Javascript functions in radians
	var dLon = Math.radians(lng - lngAddress);
	var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(Math.radians(latAddress)) * Math.cos(Math.radians(lat)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
	var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
	var d = R * c;

	return d;
}

// if departure time is at least 1 hour after arrival time
/*
 function checkForProperTimeDuration() {
 var dateFrom = $('#fromDate').val().split(' ');
 var dayFrom = parseInt(dateFrom[0].split('.')[0]);
 var monthFrom = parseInt(dateFrom[0].split('.')[1]) - 1;
 var yearFrom = parseInt(dateFrom[0].split('.')[2]);
 var hourFrom = parseInt(dateFrom[1].split(':')[0]);
 var periodFrom = parseInt(dateFrom[1].split(':')[1]);

 var dateTo = $('#toDate').val().split(' ');
 var dayTo = parseInt(dateTo[0].split('.')[0]);
 var monthTo = parseInt(dateTo[0].split('.')[1]) - 1;
 var yearTo = parseInt(dateTo[0].split('.')[2]);
 var hourTo = parseInt(dateTo[1].split(':')[0]);
 var periodTo = parseInt(dateTo[1].split(':')[1]);

 var starttime = (new Date(yearFrom, monthFrom, dayFrom, hourFrom, periodFrom, 0)).getTime();
 var endtime = (new Date(yearTo, monthTo, dayTo, hourTo, periodTo, 0)).getTime();

 if (endtime >= starttime && ((endtime / 3600000) - (starttime / 3600000)) >= 1)
 return true;
 return false;
 }*/

function renderBookingMsg(data) {
	$('.msg').html("");
	if (data == "User does not exist" || data == "Cant authenticate") {
		var msg = "Грешно потребителско име или парола!";
		$('.msg').html(msg);
	} else if (data == "Login Successful") {
		var msg = "Влязохте успещно!";
		$('.msg').html(msg);
		setTimeout(function() {
			$('.signInBox').hide();
		}, 1500);
		bookingReqeust();
	}
}

function renderConfirmMsg(data) {
	$('.msg-confirm').html("");
	if (data == "Booking completed") {
		var msg = "Запазихте успешно. Очакваме Ви!";
		$('.msg-confirm').html(msg);
		setTimeout(function() {
			$('.confirmBox').hide();
			$('.msg-confirm').html("");
		}, 2000);
	} else if (data == "already booked parkingspot here") {
		var msg = "Вече сте запазили паркомясто на този паркинг! За да запазите ново паркомясто първо трябва да отмените предната си заявка ";
		$('.msg-confirm').html(msg);
		$('.msg-confirm').append("<a href='/profile'>оттук</a>");
	} else if (data == "Not authenticated") {
		var msg = "Преди да запазите място трябва да влезете профила си!";
		$('.msg-confirm').html(msg);
	}
}

function sortAscendingByPrice(allParkings) {
	allParkings.sort(function(a, b) {
		return a.pricePerHour - b.pricePerHour;
	});
}

function ajaxCall(lat, lng) {

	/*
	 if (!checkForProperTimeDuration()) {
	 alert("Р§Р°СЃСЉС‚ РЅР° РёР·Р»РёР·Р°РЅРµ РЅРµ РјРѕР¶Рµ РґР° РїСЂРµРґС…РѕР¶РґР° С‡Р°СЃР° РЅР° РІР»РёР·Р°РЅРµ, Р° РїСЂРµСЃС‚РѕСЏС‚ Рµ РјРёРЅРёРјСѓРј Р·Р° 1 С‡Р°СЃ!");
	 return;
	 }*/

	$.ajax({
		url : "/ajaxCall/" + lat + "/" + lng,
		type : 'GET', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		//data : {id : 1, name : "ivan"},
		dataType : 'json',
		beforeSend : function() {
			$('#map').append("<img class='loadGif' style='position:fixed;top:50%;left:50%;z-index:9000;' src='/static/imgs/ajax-loader.gif' />");
		},
		success : function(data) {
			//console.log(data);
			$('.loadGif').remove();
			//parkingslen=data.filter(function(item){return item.model == "FindParking.parkingmarker";}).length;
			//methodslen=data.filter(function(item){return item.model == "FindParking.paymentmethod";}).length;
			//featureslen=data.filter(function(item){return item.model == "FindParking.parkingfeatures";}).length;

			clearLocations();
			parkings = [];
			paymentMethods = [];
			features = [];
			markers = [];

			//var splitedData = data.split("<>");
			var parkingsData = data.filter(function(item) {
				return item.model == "FindParking.parkingmarker";
			});
			var featuresData = data.filter(function(item) {
				return item.model == "FindParking.parkingfeatures";
			});
			var paymentMethodData = data.filter(function(item) {
				return item.model == "FindParking.paymentmethod";
			});

			parseAjaxParkings(parkingsData);
			parseAjaxFeatures(featuresData);
			parseAjaxMethods(paymentMethodData);

			for (var i = 0, len = parkings.length; i < len; i++) {
				createMarker(parkings[i], i);
			}
			allParkings = parkings;
			sortAscendingByPrice(allParkings);
			filterParkingsAndDisplay(allParkings);
		},
		error : function(error) {

			// Log any error.
			console.log("ERROR:", error);

		},
	});
}

//parse data returned from ajaxRequest as string (splited)
function parseAjaxParkings(ajaxParkings) {
	//var ajaxParkings = ajaxData.split('@');
	// i < len -1 becausewhen split by '@' there is a left string at the end
	for (var i = 0, len = ajaxParkings.length; i < len; i++) {
		//var parking = ajaxParkings[i].split('&');
		var currentParking = new Object();
		currentParking.id = parseInt(ajaxParkings[i].pk);
		currentParking.availableSpaces = parseFloat(ajaxParkings[i].fields['availableSpaces']);
		currentParking.name = ajaxParkings[i].fields['name'];
		currentParking.address = ajaxParkings[i].fields['address'];
		currentParking.lat = parseFloat(ajaxParkings[i].fields['lat']);
		currentParking.lng = parseFloat(ajaxParkings[i].fields['lng']);
		//currentParking.distance = parseFloat(ajaxParkings[i].fields['distance']);
		currentParking.distance = distance(markerCenter.position.lat(), markerCenter.position.lng(), currentParking.lat, currentParking.lng);
		currentParking.capacity = parseFloat(ajaxParkings[i].fields['capacity']);
		currentParking.workFrom = (parseFloat(ajaxParkings[i].fields['workFrom'])).toFixed(2);
		currentParking.workTo = (parseFloat(ajaxParkings[i].fields['workTo'])).toFixed(2);
		currentParking.pricePerHour = parseFloat(ajaxParkings[i].fields['pricePerHour']);
		currentParking.paymentMethod = parseFloat(ajaxParkings[i].fields['paymentMethod']);
		currentParking.features = parseFloat(ajaxParkings[i].fields['features']);
		parkings.push(currentParking);
	};
}

//parse data returned from ajaxRequest as string (splited)
function parseAjaxFeatures(ajaxFeatures) {
	//var ajaxFeatures = ajaxData.split('@');
	// i < len -1 becausewhen split by '@' there is a left string at the end
	for (var i = 0, len = ajaxFeatures.length; i < len; i++) {
		//var feature = ajaxFeatures[i].split('&');
		var currentFeature = new Object();
		currentFeature.elCars = ajaxFeatures[i].fields['elCars'];
		currentFeature.security = ajaxFeatures[i].fields['security'];
		currentFeature.valet = ajaxFeatures[i].fields['valet'];
		currentFeature.discount = ajaxFeatures[i].fields['discount'];
		currentFeature.SUV = ajaxFeatures[i].fields['SUV'];
		currentFeature.motor = ajaxFeatures[i].fields['motor'];
		currentFeature.carwash = ajaxFeatures[i].fields['carwash'];
		currentFeature.handicap = ajaxFeatures[i].fields['handicap'];
		currentFeature.personnel = ajaxFeatures[i].fields['personnel'];
		currentFeature.indoor = ajaxFeatures[i].fields['indoor'];
		currentFeature.id = parseInt(ajaxFeatures[i].pk);
		features.push(currentFeature);
	};
}

//parse data returned from ajaxRequest as string (splited)
function parseAjaxMethods(ajaxPMethods) {
	//var ajaxPMethods = ajaxData.split('@');
	// i < len -1 becausewhen split by '@' there is a left string at the end
	for (var i = 0, len = ajaxPMethods.length; i < len; i++) {
		//var pmethod = ajaxPMethods[i].split('&');
		var currentMethod = new Object();
		currentMethod.parkingmeter = ajaxPMethods[i].fields['parkingmeter'];
		currentMethod.creditcard = ajaxPMethods[i].fields['creditcard'];
		currentMethod.cash = ajaxPMethods[i].fields['cash'];
		currentMethod.id = parseInt(ajaxPMethods[i].pk);
		paymentMethods.push(currentMethod);
	};
}

function getSofiaParkings() {
	$.ajax({
		url : "/sofiaParkings/",
		type : 'GET', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		//data : {id : 1, name : "ivan"},
		dataType : 'json',
		beforeSend : function() {
			$('#map').append("<img class='loadGif' style='position:fixed;top:50%;left:50%;z-index:9000;' src='/static/imgs/ajax-loader.gif' />");
		},
		success : function(data) {
			//console.log(data);
			$('.loadGif').remove();
			//parkingslen=data.filter(function(item){return item.model == "FindParking.parkingmarker";}).length;
			//methodslen=data.filter(function(item){return item.model == "FindParking.paymentmethod";}).length;
			//featureslen=data.filter(function(item){return item.model == "FindParking.parkingfeatures";}).length;

			clearLocations();
			parkings = [];
			paymentMethods = [];
			features = [];
			markers = [];

			//var splitedData = data.split("<>");
			var parkingsData = data.filter(function(item) {
				return item.model == "FindParking.parkingmarker";
			});
			var featuresData = data.filter(function(item) {
				return item.model == "FindParking.parkingfeatures";
			});
			var paymentMethodData = data.filter(function(item) {
				return item.model == "FindParking.paymentmethod";
			});

			parseAjaxParkings(parkingsData);
			parseAjaxFeatures(featuresData);
			parseAjaxMethods(paymentMethodData);

			for (var i = 0, len = parkings.length; i < len; i++) {
				createMarker(parkings[i], i);
			}
			allParkings = parkings;
			sortAscendingByPrice(allParkings);
			filterParkingsAndDisplay(allParkings);
		},
		error : function(error) {

			// Log any error.
			console.log("ERROR:", error);

		},
	});
}

// sorts parkings by price in ascending or descending order
function sortParkingsByPrice() {
	if (parkings.length > 0) {
		if (document.getElementById('price').className == "bordered nonsorted" || document.getElementById('price').className == "bordered descend") {
			allParkings = parkings;
			allParkings.sort(function(a, b) {
				return a.pricePerHour - b.pricePerHour;
			});
			document.getElementById('price').className = "bordered ascend";
			filterParkingsAndDisplay(allParkings);
		} else {
			allParkings = parkings;
			allParkings.sort(function(a, b) {
				return b.pricePerHour - a.pricePerHour;
			});
			document.getElementById('price').className = "bordered descend";
			filterParkingsAndDisplay(allParkings);
		}
	}
}

// sorts parkings by distance in ascending or descending order
function sortParkingsByDistance() {
	if (parkings.length > 0) {
		if (document.getElementById('distance').className == "bordered nonsorted" || document.getElementById('distance').className == "bordered descend") {
			allParkings = parkings;
			allParkings.sort(function(a, b) {
				return a.distance - b.distance;
			});
			document.getElementById('distance').className = "bordered ascend";
			filterParkingsAndDisplay(allParkings);
		} else {
			allParkings = parkings;
			allParkings.sort(function(a, b) {
				return b.distance - a.distance;
			});
			document.getElementById('distance').className = "bordered descend";
			filterParkingsAndDisplay(allParkings);
		}
	}
}

// event when filter image is clicked on, changes the image
function filterParkings() {
	allParkings = parkings;
	filterParkingsAndDisplay(allParkings);
}

// when being filtered parkings change their markers' image and content
// remove second part of (markers[i].labelContent != "<p>N/A</p>" && markers[i].labelContent != "") when filling all info
function distinguishUnfilteredParkings(parkings) {
	for (var i = 0, len = markers.length; i < len; i++) {
		var isNotParkings = true;

		for (var j = 0, lent = parkings.length; j < lent; j++) {
			if (markers[i].lat == parkings[j].lat) {
				isNotParkings = false;
				break;
			}
		}
		if (markers[i].icon == "/static/imgs/parkingPointer.png" || markers[i].icon == "/static/imgs/parkingPointerBlurred.png") {
			if (isNotParkings) {
				if (handlers[i].isEmpty != null || handlers[i].isEmpty == undefined)
					google.maps.event.removeListener(handlers[i]);
				markers[i].icon = "/static/imgs/parkingPointerBlurred.png";
				markers[i].setMap(map);
				handlers[i].isEmpty = true;
				ib.close();
			} else {
				if (handlers[i].isEmpty == true) {
					addClickListener(markers[i], i, getParking(markers[i].position.lat()));
					markers[i].icon = "/static/imgs/parkingPointer.png";
					markers[i].setMap(map);
					handlers[i].isEmpty = null;
				}
			}
		}
	}
}

// returns the right parking by given latitude
function getParking(lat) {
	for (var i = 0, len = parkings.length; i < len; i++) {
		if (lat == parkings[i].lat)
			return parkings[i];
	};
}

// by given parking returns its equvalent marker
function getMarkerOfParking(parking) {
	for (var i = 0, len = markers.length; i < len; i++) {
		if (markers[i].position.lat() == parking.lat)
			return markers[i];
	};
}

// renders parking info on screen
// remove second part (checkIfParkingWorks(parkings[i]) && parkings[i].pricePerHour != 0)
/*
function displayFoundParkings(parkings) {
clearFilteredParkings();
for (var i = 0, len = parkings.length; i < len; i++) {
//if (checkIfParkingWorks(parkings[i]) && parkings[i].pricePerHour != 0) {
if (parkings[i].pricePerHour != 0) {
//calcPrice(parkings[i]);
var parkingDiv = document.createElement('div');
parkingDiv.className = 'displayedParking';
parkingDiv.style.cursor = 'pointer';
//var image = "<img src='/media/" + parkings[i].image + "'" + " class='parkingImage'>";
var image = "<img src='/media/images/attempt2.png' class='parkingImage'>";
var parkingAddress = parkings[i].address;
if (parkingAddress.length > 27)
parkingAddress = parkingAddress.slice(0, 27);
var address = "<p class='parkingAddress'>" + parkingAddress + "</p>";
var price = "<span class='parkingPrice'>" + parkings[i].pricePerHour + " Р»РІ" + "</span>";
//parkings[i].price
if (parkings[i].distance > 0.5)
var distance = "<span class='parkingSpaces'>" + (Math.round(parkings[i].distance * 10) / 10).toFixed(1) + " РєРј" + "</span>";
else
var distance = "<span class='parkingSpaces'>" + (parkings[i].distance).toFixed(3) * 1000 + " РјРµС‚СЂР°</span>";
parkingDiv.innerHTML = image + address + price + distance;
$(".currentParkings").append(parkingDiv);
addOnclick(parkingDiv, i, parkings);
}
}
showOrHide();
}*/

//pops or hides parkingsBar depending on its content; if empty: hides, otherwise shows up;
function showOrHide() {
	var el = $('.currentParkings').html();
	if (el == "") {
		$(".displayedParkingsBar").animate({
			'height' : 0
		}, 450);
		$('.close-parkingsBar').hide();
		$(".open-parkingsBar").show();
	} else {
		$(".displayedParkingsBar").animate({
			'height' : 137
		}, 450);
		$('.open-parkingsBar').hide();
		setTimeout(function() {
			$(".close-parkingsBar").show();
		}, 450);
	}
}

// add onclick event on parking
function addOnclick(parking, i, parkings) {
	parking.addEventListener('click', function() {
		showMarkerWindow(parkings[i], getMarkerOfParking(parkings[i]));
		leftMenu._closeMenu();
	}, false);

	//parking.addEventListener('click', function() {
	//	gnMenu._closeMenu();
	//	}, false);

}

// refresh all markers
function clearLocations() {
	ib.close();
	for (var i = 0; i < markers.length; i++) {
		markers[i].setMap(null);
	}
	markers.length = 0;
}

function clearFilteredParkings() {
	$(".currentParkings").html("");
}

function displayFoundParkings(parkings) {
	clearFilteredParkings();
	var hotCounter = 0;
	for (var i = 0, len = parkings.length; i < len; i++) {
		//if (checkIfParkingWorks(parkings[i]) && parkings[i].pricePerHour != 0) {
		if (parkings[i].pricePerHour != 0) {
			//calcPrice(parkings[i]);
			var parkingLi = document.createElement('li');
			if (parkings[i].distance > 0.5)
				if (hotCounter < 3)
					parkingLi.innerHTML = "<a class='hot'><span class='leftPad'><i class='fa fa-thumbs-o-up'></i> <i class='fa fa-car'></i>  - " + parkings[i].pricePerHour + " лв/час - " + (Math.round(parkings[i].distance * 10) / 10).toFixed(1) + " км <i class='fa fa-check'></i></span>";
				else
					parkingLi.innerHTML = "<a><span class='leftPad'><i class='fa fa-car'></i>  - " + parkings[i].pricePerHour + " лв/час - " + (Math.round(parkings[i].distance * 10) / 10).toFixed(1) + " км <i class='fa fa-check'></i></span>";
			else if (hotCounter < 3)
				parkingLi.innerHTML = "<a class='hot'><span class='leftPad'><i class='fa fa-thumbs-o-up'></i> <i class='fa fa-car'></i>  - " + parkings[i].pricePerHour + " лв/час - " + (parkings[i].distance).toFixed(3) * 1000 + " м <i class='fa fa-check'></i></span>";
			else
				parkingLi.innerHTML = "<a><span class='leftPad'><i class='fa fa-car'></i>  - " + parkings[i].pricePerHour + " лв/час - " + (parkings[i].distance).toFixed(3) * 1000 + " м <i class='fa fa-check'></i></span>";
			$(".currentParkings").append(parkingLi);
			addOnclick(parkingLi, i, parkings);
			hotCounter++;
		}
	}
	showOrHide();
}

//<li><a><span class="leftPad"><i class="fa fa-car"></i> паркомясто - 3 лв/час - 1.2 км <i class="fa fa-check"></i></span></li>

// return the right feature object by given id and features list
function getFeature(featureId, features) {
	for (var i = 0; i < features.length; i++) {
		if (features[i].id == featureId) {
			//alert(features[i]);
			//var exact_feature = features.filter(function(feature){return feature.id == featureId;});
			//alert(exact_feature.length);
			//alert(exact_feature);
			return features[i];
			break;
		}
	};
}

function checkRadioButton(id, self) {
	if (id == "security") {
		if (document.getElementById('security').checked == true) {
			document.getElementById('security').checked = false;
			self.className = 'unchecked';
		} else {
			document.getElementById('security').checked = true;
			self.className = 'checked';
		}
	}
	if (id == "carwash") {
		if (document.getElementById('carwash').checked == true) {
			document.getElementById('carwash').checked = false;
			self.className = 'unchecked';
		} else {
			document.getElementById('carwash').checked = true;
			self.className = 'checked';
		}
	}
	if (id == "indoor") {
		if (document.getElementById('indoor').checked == true) {
			document.getElementById('indoor').checked = false;
			self.className = 'unchecked';
		} else {
			document.getElementById('indoor').checked = true;
			self.className = 'checked';
		}
	}
}

// filters the parkings
function filterParkingsAndDisplay(allParkings) {
	/*if (document.getElementById('elcars').checked == true)//parking.features returns features.id
	 allParkings = allParkings.filter(function(parking) {
	 return (getFeature(parking.features, features).elCars == "True");
	 });*/
	if (document.getElementById('security').checked == true)
		allParkings = allParkings.filter(function(parking) {
			return (getFeature(parking.features, features).security == true);
		});
	/*if (document.getElementById('personnel').checked == true)
	 allParkings = allParkings.filter(function(parking) {
	 return (getFeature(parking.features, features).personnel == "True");
	 });
	 if (document.getElementById('suv').checked == true)
	 allParkings = allParkings.filter(function(parking) {
	 return (getFeature(parking.features, features).SUV == "True");
	 });*/
	if (document.getElementById('indoor').checked == true)
		allParkings = allParkings.filter(function(parking) {
			return (getFeature(parking.features, features).indoor == true);
		});
	/*if (document.getElementById('valet').checked == true)
	 allParkings = allParkings.filter(function(parking) {
	 return (getFeature(parking.features, features).valet == "True");
	 });*/
	if (document.getElementById('carwash').checked == true)
		allParkings = allParkings.filter(function(parking) {
			return (getFeature(parking.features, features).carwash == true);
		});
	/*if (document.getElementById('handicap').checked == true)
	 allParkings = allParkings.filter(function(parking) {
	 return (getFeature(parking.features, features).handicap == "True");
	 });
	 if (document.getElementById('discount').checked == true)
	 allParkings = allParkings.filter(function(parking) {
	 return (getFeature(parking.features, features).discount == "True");
	 });
	 //if (document.getElementById('motor').checked == true)
	 //allParkings = allParkings.filter(function(parking) {
	 //	return (getFeature(parking.features, features).motor == "True");
	 //});*/
	displayFoundParkings(allParkings);
	distinguishUnfilteredParkings(allParkings);
	//displayNumberOfFoundParkings(allParkings);
}

$(function() {
	$('.arrival-time').datetimepicker({
		format : 'd.m.Y H:i',
		value : getCurrentDate(false),
		dayOfWeekStart : 1,
		step : 15,
	});
});
