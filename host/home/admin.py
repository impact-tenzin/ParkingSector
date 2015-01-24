from django.contrib import admin
from home.models import HomePageNewsFeed, Viewer, ParkingOwner, Statistics, Locations, Events, ParkingReport

class TinyMCEAdmin(admin.ModelAdmin):
    class Media:
        js = ('/static/js/tiny_mce//tiny_mce.js', '/static/js/tiny_mce/textareas.js',)

class ViewerAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_display = ['email', 'name']
class LocationsAdmin(admin.ModelAdmin):    search_fields = ['name']    list_display = ['id', 'lat', 'lng', 'name', 'image']
class ParkingOwnerAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_display = ['email']  

class StatisticsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'stat']class EventsAdmin(admin.ModelAdmin):    search_fields = ['name']    list_display = ['id', 'lat', 'lng', 'name', 'image']
class ReportsAdmin(admin.ModelAdmin):    search_fields = ['lat']    list_display = ['lat', 'lng', 'value', 'time']admin.site.register(ParkingReport, ReportsAdmin)   admin.site.register(Events, EventsAdmin)admin.site.register(Locations, LocationsAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(HomePageNewsFeed, TinyMCEAdmin)
admin.site.register(Viewer, ViewerAdmin)
admin.site.register(ParkingOwner, ParkingOwnerAdmin)
