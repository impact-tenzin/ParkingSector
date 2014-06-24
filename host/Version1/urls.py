from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
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
    url(r'^findparking/$', 'FindParking.views.FindParking'),
    url(r'^sofiaParkings/$', 'FindParking.views.SofiaParkings'),
    url(r'^tinymce/', include(urlpatternstinymce)),
    url(r'^useful/$', 'useful.views.loadInfo'),
    url(r'^findparking/ajaxCall/(?P<latlng>.*)$', 'FindParking.views.ajaxCall'),
    url(r'^ajaxCall/(?P<latlng>.*)$', 'FindParking.views.ajaxCall'),
    url(r'^saveViewer/', 'FindParking.views.saveViewer'),
    url(r'^markBooking/', 'FindParking.views.markBooking'),
    url(r'^homeBooking/', 'home.views.homeBooking'),
    url(r'^actualiseNumber/', 'home.views.increaseCustomer'),
	url(r'^checkForLogin/', 'home.views.is_logged_in'),
	url(r'^bookParkingSpot/', 'parkingclient.views.BookParkingSpot'),
	url(r'^confirmBooking/', 'parkingclient.views.ConfirmBooking'),
	url(r'^getParkingRequests/', 'parkingclient.views.GetParkingRequests'),
	url(r'^deleteBooking/', 'parkingclient.views.DeleteBooking'),
	url(r'^signIn/', 'parkingclient.views.SignInBeforeBooking'),
    url(r'^login/(?P<type>.*)$', 'parkingclient.views.LoginRequest'),
	url(r'^adminpanel/(?P<type>.*)$', 'parkingclient.views.LoginRequest'),
    url(r'^logout/', 'parkingclient.views.LogoutRequest'),
    url(r'^profile/', 'parkingclient.views.Profile'),
    #url(r'^leavingDriver/', 'parkingclient.views.LeavingDriver'),
    #url(r'^arrivingDriver/', 'parkingclient.views.ArrivingDriver'),
    url(r'^useful/(?P<city>.*)$', 'useful.views.loadInfoForCity'),
             url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
