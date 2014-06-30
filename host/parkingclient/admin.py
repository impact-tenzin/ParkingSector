# -*- coding: utf-8 -*- from django.contrib import admin
from parkingclient.models import Client, RegularUser, ParkingHistory, BookedSpots, LicencePlates

class ClientAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ['id','user','parking_id']
    
class RegularUserAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ['id','user']
    
class ParkingHistoryAdmin(admin.ModelAdmin):
    ordering = ['parking_id']
    search_fields = ['licence_plate']
    list_display = ['parking_id', 'licence_plate', 'arrival_time', 'duration', 'price_list']

class BookedSpotsAdmin(admin.ModelAdmin):
    ordering = ['parking_id']
    search_fields = ['licence_plate']
    list_display = ['parking_id', 'user_id', 'licence_plate', 'arrival_time', 'duration', 'price_list']

class LicencePlatesAdmin(admin.ModelAdmin):
    search_fields = ['licence_plate']
    list_display = ['user_id', 'licence_plate']

admin.site.register(LicencePlates, LicencePlatesAdmin)
admin.site.register(BookedSpots, BookedSpotsAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(RegularUser, RegularUserAdmin)
admin.site.register(ParkingHistory, ParkingHistoryAdmin)
