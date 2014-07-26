# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User

class RegularUser(models.Model):
        user = models.OneToOneField(User)
        #licence_plate = models.ForeignKey('LicencePlates', null=True, blank=True)
        
        def __unicode__(self):
                return str(self.user)
 
class LicencePlates(models.Model):
    user_id = models.IntegerField()
    licence_plate = models.CharField(max_length = 45)
    
    def __unicode__(self):
        return str(self.licence_plate)