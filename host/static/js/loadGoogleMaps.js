var map;
function load() {
				map = new google.maps.Map(document.getElementById("map"), {
					center : new google.maps.LatLng(42.7000, 23.3333),
					zoom : 14,
					mapTypeId : google.maps.MapTypeId.ROADMAP,
					disableDefaultUI : true,
					//panControl : true,
					zoomControl : true,
					zoomControlOptions : {
						position : google.maps.ControlPosition.RIGHT_CENTER
					},
					mapTypeControl : true,
					scaleControl : true,
					streetViewControl : true,
					streetViewControlOptions : {
						position : google.maps.ControlPosition.RIGHT_CENTER
					},
					overviewMapControl : true
				});

			}