# -*- coding: utf-8 -*- 
from django.contrib import admin
from FindParking.models import ParkingMarker, ParkingFeatures, PaymentMethod, Contacts

class ParkingAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['address']
    list_display = ['id', 'features', 'paymentMethod', 'contacts','city', 'name',
                     'address', 'capacity', 'pricePerHour', 'workFrom', 'workTo', 'lat', 'lng', 'description', 'bookingCounter']

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
    list_display = ['id', 'contactNames', 'contactPosition', 'contactMail', 'contactPhone','website']
    
admin.site.register(ParkingFeatures, ParkingFeaturesAdmin)
admin.site.register(ParkingMarker, ParkingAdmin)
admin.site.register(PaymentMethod, PaymentAdmin)
admin.site.register(Contacts, ContactsAdmin)