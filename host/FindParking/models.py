# -*- coding: utf-8 -*- 
from django.db import models

class ParkingMarker(models.Model):
    """
    model for table that will store the parkings and their information
    two foreign keys: for parkings' features and payment method
    """
    name = models.CharField(max_length=50,null = True, blank=True)
    address = models.CharField(max_length=120,null = True, blank=True)
    capacity = models.IntegerField(null = True, blank=True,default = 0)
    pricePerHour = models.FloatField(null = True, blank=True)
    #image = models.ImageField(upload_to='images/',default = 'images/noPhoto_camera3.png')
    availableSpaces = models.IntegerField(null = True, blank=True,default = 0)
    workFrom = models.FloatField(null = True, blank=True)
    workTo = models.FloatField(null = True, blank=True)
    lat = models.FloatField()
    lng = models.FloatField()
    description = models.TextField(null = True, blank=True)
    city = models.CharField(max_length=50,null = True, blank=True)
    bookingCounter = models.IntegerField(null = True, blank=True, default = 0)
    supportsBooking = models.BooleanField(default=False)
    isPublic = models.BooleanField(default=False)
    features = models.ForeignKey('ParkingFeatures',null = True, blank=True,default = 1)
    paymentMethod = models.ForeignKey('PaymentMethod',null = True, blank=True,default = 1)
    contacts = models.ForeignKey('Contacts',null = True, blank=True,default = 1)
    priceList = models.ForeignKey('PriceList',null = True, blank=True,default = 1)
    
    def __unicode__(self):
        return self.address
  
    def get_lat(self):
        return self.lat;
    
    def get_lng(self):
        return self.lng;

class PriceList(models.Model):
    oneHour = models.FloatField(default = -1)
    twoHours = models.FloatField(default = -1)
    threeHours = models.FloatField(default = -1)
    fourHours = models.FloatField(default = -1)
    fiveHours = models.FloatField(default = -1)
    sixHours = models.FloatField(default = -1)
    sevenHours = models.FloatField(default = -1)
    eightHours = models.FloatField(default = -1)
    nineHours = models.FloatField(default = -1)
    tenHours = models.FloatField(default = -1)
    elevenHours = models.FloatField(default = -1)
    twelveHours = models.FloatField(default = -1)
    
    def __unicode__(self):
        return unicode(str(self.id))
 
class ParkingFeatures(models.Model):
    """
    model for table that will store the parkigns' features
    """
    elCars = models.BooleanField()
    security = models.BooleanField()
    valet = models.BooleanField()
    discount = models.BooleanField()
    SUV = models.BooleanField()
    motor = models.BooleanField()
    carwash = models.BooleanField()
    personnel = models.BooleanField()
    handicap = models.BooleanField()
    indoor = models.BooleanField()
    
    def __unicode__(self):
        return unicode(str(self.id))
    
class PaymentMethod(models.Model):
    """
    model for table that will store the payment methods that a particular parking offers
    """
    parkingmeter = models.BooleanField()
    creditcard = models.CharField(max_length=50,null = True, blank=True,default = '--')
    cash = models.BooleanField()
    
    def __unicode__(self):
        return unicode(str(self.id))
    
class Contacts(models.Model):
    """
    model for table that will store contacs for each parking
    """
    contactNames = models.CharField(max_length=50,null = True, blank=True)
    contactPosition = models.CharField(max_length=50,null = True, blank=True)
    contactMail = models.CharField(max_length=50,null = True, blank=True)
    contactPhone = models.CharField(max_length=50,null = True, blank=True)
    website = models.CharField(max_length=50,null = True, blank=True)
    
    def __unicode__(self):
        return unicode(str(self.id))
    
class Feedback(models.Model):
    booking = models.CharField(max_length=5,null = True, blank=True)
    freeSpaces = models.CharField(max_length=5,null = True, blank=True)
    other = models.TextField(null = True, blank=True)
    useful = models.CharField(max_length=5,null = True, blank=True)
    notUseful = models.CharField(max_length=5,null = True, blank=True)

    def __unicode__(self):
        return unicode(str(self.id))
    
class ParkingRequest(models.Model):
    user_id = models.IntegerField()
    pricePerHour = models.CharField(max_length=10,null = True, blank=True)
    workHours = models.CharField(max_length=12,null = True, blank=True)
    lat = models.CharField(max_length=12)
    lng = models.CharField(max_length=12)
    type = models.CharField(max_length=5,null = True, blank=True)
    features = models.CharField(max_length=35,null = True, blank=True)
    
    def __unicode__(self):
        return unicode(str(self.id))
    
