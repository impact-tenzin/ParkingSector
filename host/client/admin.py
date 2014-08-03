# -*- coding: utf-8 -*- 
from client.models import Client, ParkingHistory, BookedSpots, ParkingHistory, ErrorHistory

class ClientAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ['id','user','parking_id']
class ParkingHistoryAdmin(admin.ModelAdmin):
    ordering = ['parking_id']
    search_fields = ['licence_plate']
    list_display = ['parking_id', 'licence_plate', 'arrival_time', 'duration', 'price_list']

class BookedSpotsAdmin(admin.ModelAdmin):
    ordering = ['parking_id']
    search_fields = ['licence_plate']
    list_display = ['parking_id', 'user_id', 'licence_plate', 'arrival_time', 'duration', 'price_list']
admin.site.register(BookedSpots, BookedSpotsAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ParkingHistory, ParkingHistoryAdmin)