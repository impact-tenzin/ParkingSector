from django.db import models

class HomePageNewsFeed(models.Model):
    info = models.TextField()
    title = models.CharField(max_length=45)
    def __unicode__(self):
        return str(self.title)

class Viewer(models.Model):
    email = models.CharField(max_length = 60)
    name = models.CharField(max_length = 60)
    
class ParkingOwner(models.Model):
    email = models.CharField(max_length = 60)
    
class Statistics(models.Model):
    name = models.CharField(max_length = 50)
    stat = models.IntegerField()
    
class Locations(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length = 100)
    image = models.CharField(max_length = 50)
    
class Events(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length = 100)
    image = models.CharField(max_length = 50)
    
class ParkingReport(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    value = models.IntegerField()
    time = models.DateTimeField()