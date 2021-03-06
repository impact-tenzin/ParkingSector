# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User

class RegularUser(models.Model):
        user = models.OneToOneField(User)
        fb_email = models.EmailField(blank=True)
        fb_name = models.CharField(max_length=45, blank=True)
        fb_id = models.CharField(max_length=16)
        #fb_token = models.CharField(max_length=45)
        #licence_plate = models.ForeignKey('LicencePlates', null=True, blank=True)
        
        def __unicode__(self):
                return str(self.user)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    activation_key = models.CharField(max_length=20)

class LicencePlates(models.Model):
    user_id = models.IntegerField()
    licence_plate = models.CharField(max_length = 45)
    
    def __unicode__(self):
        return str(self.licence_plate)
    
class ParkingReview(models.Model):
        parking_id = models.IntegerField()
        username = models.CharField(max_length=20)
        fb_id = models.CharField(max_length=16, null=True, blank=True)
        review = models.TextField()
        date = models.CharField(max_length=16)
        
        def __unicode__(self):
                return unicode(self.id)
            
class ParkingRating(models.Model):
        parking_id = models.IntegerField()
        raters = models.IntegerField()
        rating = models.FloatField()
   
        def __unicode__(self):
                return unicode(self.id)