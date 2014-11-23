function testAPI() {
	//console.log('Welcome!  Fetching your information.... ');
	FB.api('/me', function(response) {
		//alert('Successful login for: ' + response.name + " email: " + response.email);
		//document.getElementById('status').innerHTML = 'Thanks for logging in, ' + response.name + '!';
		login_or_register(response.email, response.name, response.id)
	});
}

function login_or_register(email, username, id) {
	$.ajax({
		url : "/loginOrRegister/",
		type : 'POST', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		data : {
			username : username,
			email : email,
			fb_id : id,
			csrfmiddlewaretoken : '{{ csrf_token }}'
		},
		success : function(data) {
			if (data == 'fblogin complete' || data == "registration with fb complete") {
				get_fb_id();
				var msg = "Влязохте успешно!";
				$('.msg').html(msg);
				setTimeout(function() {
					$('.signInBox').hide();
					//bookingRequest();
				}, 1500);
			} else
				alert(data);
		},
		error : function(error) {
			// Log any error.
			console.log("ERROR:", error);
		},
	});
}

$('#loginFormPassword').keydown(function(event) {

	var keypressed = event.keyCode || event.which;

	if (keypressed == 13) {

		$(".signInButton").trigger("click");

	}

});

function renderBookingMsg(data) {
	$('.msg').html("");
	if (data == "User does not exist" || data == "Cant authenticate") {
		var msg = "Грешно потребителско име или парола!";
		$('.msg').html(msg);
	} else if (data == "Login Successful") {
		var msg = "Влязохте успешно!";
		$('.msg').html(msg);
		setTimeout(function() {
			$('.signInBox').hide();
			//bookingRequest();
		}, 1500);
	}
}

function signIn() {
				$.ajax({
					url : "/signIn/",
					type : 'POST', //this is the default though, you don't actually need to always mention it
					xhrFields : {
						withCredentials : true
					},
					headers : {
						'X-Requested-With' : 'XMLHttpRequest'
					},
					data : {
						name : $('.sign-name').val(),
						pass : $('.sign-pass').val(),
					},
					dataType : 'html',

					success : function(data) {
						renderBookingMsg(data);
						addDropDownToPicture();
					},
					error : function(error) {

						// Log any error.
						console.log("ERROR:", error);

					},
				});
			}

function addDropDownToPicture()
{
	$(".dropdownOptions").attr("class", "dropdown-menu dropdownOptions");
	//$(".dropdownOptions").show();
}

function get_fb_id() {
	$.ajax({
		url : "/getFbId/",
		type : 'GET', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		success : function(data) {
			if (data.length > 0) {
				$("#i").remove();
				var src = "https://graph.facebook.com/" + data + "/picture";
				$("#my_image").attr("src", src);
				addDropDownToPicture();
			}
		},
		error : function(error) {
			// Log any error.
			console.log("ERROR:", error);
		},
	});
}

function closeSignIn() {
	$('.signInBox').hide();
	$('.msg').html("");
}

function checkForLogin() {
			$.ajax({
				url : "/checkForLogin/",
				type : 'GET', //this is the default though, you don't actually need to always mention it
				xhrFields : {
					withCredentials : true
				},
				headers : {
					'X-Requested-With' : 'XMLHttpRequest'
				},
				dataType : 'html',
				success : function(data) {
					if (data == "Authenticated")
						addParking();
					else
						$(".signInBox").show();
				},
				error : function(error) {

					// Log any error.
					console.log("ERROR:", error);

				},
			});
		}