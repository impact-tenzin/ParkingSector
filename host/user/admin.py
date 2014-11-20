# -*- coding: utf-8 -*- from django.contrib import admin
from user.models import RegularUser, LicencePlates, ParkingReview

class RegularUserAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ['id','user']
    
class LicencePlatesAdmin(admin.ModelAdmin):
    search_fields = ['licence_plate']
    list_display = ['user_id', 'licence_plate']class ParkingReviewAdmin(admin.ModelAdmin):    search_fields = ['id']    list_display = ['parking_id', 'review', 'date', 'username', 'fb_id']
admin.site.register(ParkingReview, ParkingReviewAdmin)
admin.site.register(LicencePlates, LicencePlatesAdmin)admin.site.register(RegularUser, RegularUserAdmin)