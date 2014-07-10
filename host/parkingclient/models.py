# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
        user = models.OneToOneField(User)
        parking_id = models.IntegerField()

        def __unicode__(self):
                return str(self.parking_id)

class RegularUser(models.Model):
        user = models.OneToOneField(User)
        #licence_plate = models.ForeignKey('LicencePlates', null=True, blank=True)
        
        def __unicode__(self):
                return str(self.user)

class ParkingHistory(models.Model):
    parking_id = models.IntegerField()
    user_id = models.IntegerField()
    licence_plate = models.CharField(max_length=45)
    arrival_time = models.CharField(max_length=45)
    duration = models.CharField(max_length=45)
    price_list = models.CharField(max_length=45)
    
    def __unicode__(self):
        return str(self.parking_id)
    
class BookedSpots(models.Model):
    parking_id = models.IntegerField()
    user_id = models.IntegerField()
    price_list = models.CharField(max_length=70)
    parking_address = models.CharField(max_length=45)
    licence_plate = models.CharField(max_length = 45)
    duration = models.CharField(max_length = 45)
    arrival_time = models.CharField(max_length = 45)
    
    def __unicode__(self):
        return str(self.parking_id)
    
class LicencePlates(models.Model):
    user_id = models.IntegerField()
    licence_plate = models.CharField(max_length = 45)
    
    def __unicode__(self):
        return str(self.licence_plate)

class ErrorHistory(models.Model):
    description = models.TextField()  