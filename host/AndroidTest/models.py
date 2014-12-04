# -*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User

class MobileSession(models.Model):
    user = models.OneToOneField(User)
    session_key = models.CharField(max_length=30)

    def __unicode__(self):
        return str(self.user)