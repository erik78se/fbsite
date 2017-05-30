# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models
from happenings.models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import URLValidator

#
# Extending 'happenings' calendar events here
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
#
class FacebookEvent(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    facebook_event_id = models.IntegerField(unique=True)
    facebook_cover_image_url = models.TextField(validators=[URLValidator()], default='http://image.png')

    def __str__(self):
        return "[{}] {}".format(self.facebook_event_id, self.event)
        
    def __unicode__(self):
        return u"[{}] {}".format(self.facebook_event_id, self.event)
