from django.conf.urls import patterns, include, url

android_public_patterns = patterns('',
    #url(r'^android_sofiaParkings/$', 'Android.android_controls.sofia_parkings'),
    url(r'^android_ajaxCall/(?P<latlng>.*)$', 'Android.android_controls.ajax_call'),
    url(r'^android_loginUser/$', 'Android.android_controls.login_request'),
    url(r'^android_fblogin/$', 'Android.android_controls.facebook_login'),
    url(r'^android_resetPassword/$', 'Android.android_controls.reset_password'),
    url(r'^android_register/$', 'Android.android_controls.create_regular_user'),
    url(r'^android_resetEmail/$', 'Android.android_controls.check_for_valid_email'),
    url(r'^android_confirmBooking/$', 'Android.android_controls.confirm_booking'),
    url(r'^android_cancelBooking/$', 'Android.android_controls.cancel_booking'),
    url(r'^android_logoutUser/$', 'Android.android_controls.logout_request'),
    url(r'^android_getBookingRequests/$', 'Android.android_controls.get_booking_requests'),
    url(r'^android_getLicencePlates/$', 'Android.android_controls.get_licence_plates'),
    url(r'^android_removeLicencePlate/$', 'Android.android_controls.remove_licence_plate'),
    url(r'^android_addLicencePlate/$', 'Android.android_controls.add_licence_plate'),
    url(r'^android_getUsername/$', 'Android.android_controls.get_username'),
)