from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from AndroidTest.android_test_urls import android_test_patterns
from Android.android_public_urls import android_public_patterns
import registration
from django.contrib.auth import views as auth_views
import os
admin.autodiscover()
def fromRelativePath(*relativeComponents):
    return os.path.join(os.path.dirname(__file__), *relativeComponents).replace("\\", "/")

urlpatternstinymce = patterns('tinymce.views',
    url(r'^js/textareas/(?P<name>.+)/$', 'textareas_js', name='tinymce-js'),
    url(r'^js/textareas/(?P<name>.+)/(?P<lang>.*)$', 'textareas_js', name='tinymce-js-lang'),
    url(r'^spellchecker/$', 'spell_check'),
    url(r'^flatpages_link_list/$', 'flatpages_link_list'),
    url(r'^compressor/$', 'compressor', name='tinymce-compressor'),
    url(r'^filebrowser/$', 'filebrowser', name='tinymce-filebrowser'),
    url(r'^preview/(?P<name>.+)/$', 'preview', name='tinymce-preview'),
)

urlpatterns = patterns('',
    #url(r'^testErrorMessages/', 'client.views.test_error_messages'),
    #url(r'^useful/$', 'useful.views.home', name='home'),
    #url(r'^add_socket_id/$', 'useful.views.add_socket_id'),
    #url(r'^m/?$', 'useful.views.message', name='message'),
    #url("", include('django_socketio.urls')),
    url(r'^$', 'home.views.home'),
    url(r'^getLocation/$', 'home.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url("^admin-media/(?P<path>.*)$",
    "django.views.static.serve",
    {"document_root": fromRelativePath("media", "admin-media")}),
    #url(r'^findparking/$', 'FindParking.views.find_parking'),
    #url(r'^sofiaParkings/$', 'FindParking.views.sofia_parkings'),
    url(r'^tinymce/', include(urlpatternstinymce)),
    #url(r'^useful/$', 'useful.views.loadInfo'),
    url(r'^findparking/ajaxCall/(?P<latlng>.*)$', 'FindParking.views.ajax_call'),
    url(r'^ajaxCall/(?P<latlng>.*)$', 'FindParking.views.ajax_call'),
    #url(r'^saveViewer/', 'FindParking.views.save_viewer'),
    #url(r'^markBooking/', 'FindParking.views.mark_booking'),
    #url(r'^homeBooking/', 'home.views.home_booking'),
    #url(r'^actualiseNumber/', 'home.views.increase_customer'),
	url(r'^checkForLogin/', 'home.views.is_logged_in'),
    url(r'^getFbId/', 'user.views.get_fb_id'),
	#url(r'^bookParkingSpot/', 'user.views.booking_parkingspot'),
	#url(r'^confirmBooking/', 'user.views.confirm_booking'),
	#url(r'^getParkingRequests/', 'client.views.get_parking_requests'),
	#url(r'^cancelBooking/', 'user.views.cancel_booking'),
    #url(r'^cancelBookingAdmin/', 'client.views.cancel_booking_admin'),
	url(r'^signIn/', 'user.views.signin_before_booking'),
    url(r'^login/(?P<type>.*)$', 'user.views.login_request'),
    url(r'^loginOrRegister/', 'user.views.facebook_login'),
    url(r'^syncWithFB/', 'user.views.facebook_sync'),
    url(r'^register/', 'user.views.register_user'),
    #url(r'^registerfb/', 'user.views.register_user_with_fb'),
    url(r'^confirm/(?P<activation_key>.*)/(?P<user_id>.*)', 'user.email_confirmation.confirm'),
    url(r'^error_page/', 'user.views.display_error_page'),
	url(r'^adminpanel/(?P<type>.*)$', 'user.views.login_request'),
    url(r'^logout/', 'user.views.logout_request'),
    url(r'^profile/', 'user.views.profile'),
    #url(r'^pricelist/', 'client.views.render_price_list_page'),
    #url(r'^getPriceList/', 'client.views.get_price_list'),
    #url(r'^getBookingRequests/', 'user.views.get_booking_requests'),
    #url(r'^actualisePriceList/', 'client.views.actualise_price_list'),
    #url(r'^saveParkingInHistory/', 'client.views.save_parking_info'),
    #url(r'^addNewPlate/', 'user.views.add_licence_plate'),
    #url(r'^removeLicencePlate/', 'user.views.remove_licence_plate'),
    #url(r'^actualiseAvailableSpaces/', 'client.views.actualise_available_spaces'),
    url(r'^showParkingsAroundDestination/(?P<latlng>.*)$', 'home.views.redirect_to_map_from_destination'),
    url(r'^showParkingsAroundEvent/(?P<latlng>.*)$', 'home.views.redirect_to_map_from_event'),
    url(r'^password/reset/$', 'user.views.render_password_reset_form'),
    url(r'^resetpassword/(?P<activation_key>.*)/(?P<user_id>.*)', 'user.views.password_reset'),
    url(r'^checkForValidEmail/$', 'user.views.check_for_valid_email'),
    url(r'^setNewPassword/$', 'user.email_confirmation.set_new_password'),
    url(r'^saveFeedback/$', 'FindParking.views.save_feedback'),
    url(r'^addParking/$', 'FindParking.views.add_parking'),
    url(r'^addParkingView/$', 'FindParking.views.add_parking_view'),
    url(r'^addParkingReview/$', 'user.views.save_review'),
    url(r'^getParkingReviews/$', 'user.views.get_reviews'),
    url(r'^getRating/$', 'user.views.get_rating'),
    url(r'^addRating/$', 'user.views.add_rating'),
    #url(r'^leavingDriver/', 'parkingclient.views.LeavingDriver'),
    #url(r'^arrivingDriver/', 'parkingclient.views.ArrivingDriver'),
    #override the default urls
    #url(r'^password/change/$',
    #                auth_views.password_change,
    #                name='password_change'),
    #url(r'^password/change/done/$',
    #                auth_views.password_change_done,
    #                name='password_change_done'),
    #url(r'^password/reset/$',
    #                auth_views.password_reset,
    #                name='password_reset'),
    #url(r'^password/reset/done/$',
    #                auth_views.password_reset_done,
    #                name='password_reset_done'),
    #url(r'^password/reset/complete/$',
    #                auth_views.password_reset_complete,
    #                name='password_reset_complete'),
    #url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #                auth_views.password_reset_confirm,
    #                name='password_reset_confirm'),
      #and now add the registration urls
    #url(r'', include('registration.urls')),
    #url(r'^useful/(?P<city>.*)$', 'useful.views.loadInfoForCity'),
            # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            #'document_root': settings.MEDIA_ROOT,
        #}),
)

urlpatterns += android_public_patterns 
urlpatterns += android_test_patterns 