from django.db import models

class UsefulInformation(models.Model):
    info = models.TextField()
    title = models.CharField(max_length=50)
    
    def __unicode__(self):
        return(self.title)
