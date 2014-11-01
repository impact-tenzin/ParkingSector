function saveFeedback() {
	if (!$("#booking").prop("checked") && !$("#other").prop("checked") && !$("#freespaces").prop("checked") && !$("#useful").prop("checked") && !$("#notuseful").prop("checked")) {
		return;
	}

	if ($("#booking").prop("checked")) var booking = "yes"
	else var booking = "--";
	if ($("#freespaces").prop("checked")) var freespaces = "yes"
	else var freespaces = "--";
	if ($("#other").prop("checked")) var other = $("#solution").val()
	else var other = "";
	if ($("#useful").prop("checked")) var useful = "yes"
	else var useful = "--";
	if ($("#notuseful").prop("checked")) var notuseful = "yes"
	else var notuseful = "--";
	
	if(booking == "--" && freespaces == "--" && useful == "--" && notuseful == "--" && other == "") return;
	
	sendFeedbackData1(booking, freespaces, other, useful, notuseful);

}

function saveFeedback2() {
	if (!$("#booking2").prop("checked") && !$("#other2").prop("checked") && !$("#freespaces2").prop("checked") && !$("#useful2").prop("checked") && !$("#notuseful2").prop("checked")) {
		return;
	}

	if ($("#booking2").prop("checked")) var booking = "yes"
	else var booking = "--";
	if ($("#freespaces2").prop("checked")) var freespaces = "yes"
	else var freespaces = "--";
	if ($("#other2").prop("checked")) var other = $("#solution2").val()
	else var other = "";
	if ($("#useful2").prop("checked")) var useful = "yes"
	else var useful = "--";
	if ($("#notuseful2").prop("checked")) var notuseful = "yes"
	else var notuseful = "--";
	
	if(booking == "--" && freespaces == "--" && useful == "--" && notuseful == "--" && other == "") return;
	
	sendFeedbackData2(booking, freespaces, other, useful, notuseful);

}

function sendFeedbackData1(booking, freespaces, other, useful, notuseful)
{
	$.ajax({
		url : "/saveFeedback/",
		type : 'POST', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		data : {
			booking : booking,
			freeSpaces : freespaces,
			other : other,
			useful : useful,
			notUseful : notuseful
		},
		success : function(data) {
			$('.solution').hide();
			$('.feedback').html("<div class='thank-you'>Благодарим Ви!</div>");
			setTimeout(function() {
				$('.bgy').hide();
				$('.feedback').hide();
			}, 3000);
		},
		error : function(error) {
			// Log any error.
			console.log("ERROR:", error);

		},
	});
}

function sendFeedbackData2(booking, freespaces, other, useful, notuseful)
{
	$.ajax({
		url : "/saveFeedback/",
		type : 'POST', //this is the default though, you don't actually need to always mention it
		xhrFields : {
			withCredentials : true
		},
		headers : {
			'X-Requested-With' : 'XMLHttpRequest'
		},
		data : {
			booking : booking,
			freeSpaces : freespaces,
			other : other,
			useful : useful,
			notUseful : notuseful
		},
		success : function(data) {
			$('.solution2').hide();
			$('.feedbackholder').html("<div class='thank-you2'>Благодарим Ви!</div>");
			setTimeout(function() {
				$('.bgy').hide();
				$('.feedbackholder').hide();
			}, 3000);
		},
		error : function(error) {
			// Log any error.
			console.log("ERROR:", error);

		},
	});
}

function showTextbox()
{
	if($("#other").prop("checked"))
		$('.solution').show();
	else
		$('.solution').hide();
}

function showTextbox2()
{
	if($("#other2").prop("checked"))
		$('.solution2').show();
	else
		$('.solution2').hide();
}