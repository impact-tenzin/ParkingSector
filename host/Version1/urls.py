from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import registration
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
    #url("", include('django_socketio.urls')),
    url(r'^$', 'home.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url("^admin-media/(?P<path>.*)$",
    "django.views.static.serve",
    {"document_root": fromRelativePath("media", "admin-media")}),
    url(r'^findparking/$', 'FindParking.views.find_parking'),
    url(r'^sofiaParkings/$', 'FindParking.views.sofia_parkings'),
    url(r'^tinymce/', include(urlpatternstinymce)),
    url(r'^useful/$', 'useful.views.loadInfo'),
    url(r'^findparking/ajaxCall/(?P<latlng>.*)$', 'FindParking.views.ajax_call'),
    url(r'^ajaxCall/(?P<latlng>.*)$', 'FindParking.views.ajax_call'),
    url(r'^saveViewer/', 'FindParking.views.save_viewer'),
    url(r'^markBooking/', 'FindParking.views.mark_booking'),
    url(r'^homeBooking/', 'home.views.home_booking'),
    url(r'^actualiseNumber/', 'home.views.increase_customer'),
	url(r'^checkForLogin/', 'home.views.is_logged_in'),
	url(r'^bookParkingSpot/', 'parkingclient.views.booking_parkingspot'),
	url(r'^confirmBooking/', 'parkingclient.views.confirm_booking'),
	url(r'^getParkingRequests/', 'parkingclient.views.get_parking_requests'),
	url(r'^cancelBooking/', 'parkingclient.views.cancel_booking'),
	url(r'^signIn/', 'parkingclient.views.signin_before_booking'),
    url(r'^login/(?P<type>.*)$', 'parkingclient.views.login_request'),
	url(r'^adminpanel/(?P<type>.*)$', 'parkingclient.views.login_request'),
    url(r'^logout/', 'parkingclient.views.logout_request'),
    url(r'^profile/', 'parkingclient.views.profile'),
    #url(r'^leavingDriver/', 'parkingclient.views.LeavingDriver'),
    #url(r'^arrivingDriver/', 'parkingclient.views.ArrivingDriver'),
    #override the default urls
    url(r'^password/change/$',
                    auth_views.password_change,
                    name='password_change'),
    url(r'^password/change/done/$',
                    auth_views.password_change_done,
                    name='password_change_done'),
    url(r'^password/reset/$',
                    auth_views.password_reset,
                    name='password_reset'),
    url(r'^password/reset/done/$',
                    auth_views.password_reset_done,
                    name='password_reset_done'),
    url(r'^password/reset/complete/$',
                    auth_views.password_reset_complete,
                    name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                    auth_views.password_reset_confirm,
                    name='password_reset_confirm'),
      #and now add the registration urls
    url(r'', include('registration.urls')),
    url(r'^useful/(?P<city>.*)$', 'useful.views.loadInfoForCity'),
             url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
