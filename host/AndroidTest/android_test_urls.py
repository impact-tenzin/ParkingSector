from django.conf.urls import patterns, include, url

android_test_patterns = patterns('',
    #url(r'^android_sofiaParkings/$', 'Android.android_controls.sofia_parkings'),
    url(r'^android_test_ajaxCall/(?P<latlng>.*)$', 'AndroidTest.android_controls.ajax_call'),
    url(r'^android_test_loginUser/$', 'AndroidTest.android_controls.login_request'),
    url(r'^android_test_fblogin/$', 'AndroidTest.android_controls.facebook_login'),
    url(r'^android_test_resetPassword/$', 'AndroidTest.android_controls.reset_password'),
    url(r'^android_test_register/$', 'AndroidTest.android_controls.create_regular_user'),
    url(r'^android_test_resetEmail/$', 'AndroidTest.android_controls.check_for_valid_email'),
    url(r'^android_test_confirmBooking/$', 'AndroidTest.android_controls.confirm_booking'),
    url(r'^android_test_cancelBooking/$', 'AndroidTest.android_controls.cancel_booking'),
    url(r'^android_test_logoutUser/$', 'AndroidTest.android_controls.logout_request'),
    url(r'^android_test_getBookingRequests/$', 'AndroidTest.android_controls.get_booking_requests'),
    url(r'^android_test_getLicencePlates/$', 'AndroidTest.android_controls.get_licence_plates'),
    url(r'^android_test_removeLicencePlate/$', 'AndroidTest.android_controls.remove_licence_plate'),
    url(r'^android_test_addLicencePlate/$', 'AndroidTest.android_controls.add_licence_plate'),
    url(r'^android_test_getUsername/$', 'AndroidTest.android_controls.get_username'),
)