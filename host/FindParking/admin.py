# -*- coding: utf-8 -*- 
from django.contrib import admin
from FindParking.models import ParkingMarker, ParkingFeatures, PaymentMethod, Contacts, PriceList, Feedback, ParkingRequest

class ParkingAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['address']
    list_display = ['id', 'features', 'paymentMethod', 'priceList', 'contacts','city', 'name',
                     'address', 'capacity', 'pricePerHour', 'workFrom', 'workTo', 'lat', 'lng', 'description', 'supportsBooking','bookingCounter', 'isPublic']
class PriceListAdmin(admin.ModelAdmin):    ordering = ['id']    search_fields = ['id']    list_display = ['id', 'oneHour', 'twoHours', 'threeHours', 'fourHours','fiveHours', 'sixHours',                     'sevenHours', 'eightHours', 'nineHours', 'tenHours', 'elevenHours', 'twelveHours']
class ParkingFeaturesAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['id']
    list_display = ['id', 'elCars', 'security', 'valet', 'discount', 'SUV', 'motor', 'carwash', 'personnel', 'handicap', 'indoor']

class PaymentAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['id']
    list_display = ['id', 'parkingmeter', 'creditcard', 'cash']

class ContactsAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['id']
    list_display = ['id', 'contactNames', 'contactPosition', 'contactMail', 'contactPhone','website']class FeedbackAdmin(admin.ModelAdmin):    ordering = ['id']    search_fields = ['id']    list_display = ['id', 'booking', 'freeSpaces', 'other', 'useful','notUseful']
class ParkingRequestAdmin(admin.ModelAdmin):    ordering = ['id']    search_fields = ['id']    list_display = ['id', 'user_id', 'lat', 'lng', 'type', 'workHours', 'pricePerHour','features']admin.site.register(ParkingRequest, ParkingRequestAdmin)  admin.site.register(Feedback, FeedbackAdmin)   admin.site.register(PriceList, PriceListAdmin)
admin.site.register(ParkingFeatures, ParkingFeaturesAdmin)
admin.site.register(ParkingMarker, ParkingAdmin)
admin.site.register(PaymentMethod, PaymentAdmin)
admin.site.register(Contacts, ContactsAdmin)