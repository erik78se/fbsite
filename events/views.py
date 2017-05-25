# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import FaceBookEventForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.shortcuts import render_to_response
from open_facebook.api import (OpenFacebook, FacebookConnection,
                               FacebookAuthorization)

from .models import  FacebookEvent
from happenings.models import Event as HappeningEvent
from happenings.models import Location as HappeningLocation
from django.contrib.auth.models import User


# Facebook API access tokens
# https://developers.facebook.com/docs/facebook-login/access-tokens/#apptokens

# GOOOD example: https://github.com/tschellenbach/Django-facebook/tree/master/facebook_example/facebook_example


def index(request):
    events =  HappeningEvent.objects.all()
    facebook_events = FacebookEvent.objects.all()
    # [u'description', u'start_time', u'place', u'end_time', u'id', u'name']
    
    for i in events:
        print(i.facebookevent.facebook_cover_image_url)

    return render_to_response('index.tmpl', {'events': events, 'fbevents': facebook_events })


def register_facebook_event(request):
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FaceBookEventForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            eid = form.cleaned_data['facebook_event_id']
            
            event_dict = {}
            event_pic = {}

            try:
                
                event_dict = get_facebook_event( eid )
           
                event_pic = get_picture_for_event( eid )
                
            except(Exception):
                
                return HttpResponse("Could not get the event. Is it private?")
            
                
            he = HappeningEvent(title=event_dict['name'], 
                                start_date=event_dict['start_time'],
                                end_date=event_dict['end_time'],
                                description=event_dict['description'],
                                created_by=User.objects.get(pk=1),
                                )
            he.save()

            if 'place' in event_dict:
                lo = event_dict.get('place')
                # h = HappeningLocation.objects.get(name=lo.name)
                


            if 'street' in event_dict.get('place', {}).get('location', {}):
                st = event_dict.get('place', {}).get('location', {}).get('street')
                print(st)

                # if street in event_dict['place']['location']['street']:
                l = HappeningLocation.objects.create(name=event_dict['place']['location']['street'],
                                                     address_line_1=event_dict['place']['location']['street'])
                he.location.add(l)

            # he.save()
            
            # Create the record of the event
            FacebookEvent.objects.create( event=he, facebook_event_id=eid , facebook_cover_image_url=event_pic['cover']['source'])
        
    # Not a POST call
    else:

        form = FaceBookEventForm()
        
    return render(request, 'register_event.html', {'form': form})


def get_facebook_event(fbevent_id):
    """ 
    Gets facebook events from facebook.
    The access token is taken from site settings.py via open_facebook
    """
    app_token = FacebookAuthorization.get_app_access_token()

    graph = OpenFacebook(app_token)
    
    event = graph.get(fbevent_id)
    
    return event

def get_picture_for_event(fbevent_id):

    app_token = FacebookAuthorization.get_app_access_token()

    graph = OpenFacebook(app_token)
    
    # Getting the picture
    cover = graph.get(fbevent_id, version="v2.9", fields='cover')

    print(cover['cover']['source'])

    return cover
