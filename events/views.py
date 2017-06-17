# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import FaceBookEventForm
from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.shortcuts import render_to_response
from open_facebook.api import (OpenFacebook, FacebookConnection,
                               FacebookAuthorization)

from .models import  FacebookEvent
from happenings.models import Event as HappeningEvent
from happenings.models import Location as HappeningLocation
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

from django.contrib.auth.models import User

import logging


# Facebook API access tokens
# https://developers.facebook.com/docs/facebook-login/access-tokens/#apptokens

# GOOOD example: https://github.com/tschellenbach/Django-facebook/tree/master/facebook_example/facebook_example

logger = logging.getLogger(__name__)


def index(request):
    events =  HappeningEvent.objects.all()
    facebook_events = FacebookEvent.objects.all()    
    return render_to_response('index.html', {'events': events, 'fbevents': facebook_events })

def tourism(request):
    return render_to_response('tourism.html')

def aker(request):
    return render_to_response('aker.html')

def register_facebook_event(request):
    logger.debug("register_facebook_event called")
    eid = None
    success = False
    try:
        with transaction.atomic():
            if request.method == 'POST':
        # create a form instance and populate it with data from the request:
                form = FaceBookEventForm(request.POST)
        # check whether it's valid:
                if form.is_valid():
            # process the data in form.cleaned_data as required
                    eid = form.cleaned_data['facebook_event_id']
            
                    event_dict = {}
                    event_pic = {}
                
                    # Get Facebook event from the ID
                    event_dict = get_facebook_event( eid )
           
                    # Get the Facebook picture from the event ID
                    event_pic = get_picture_for_event( eid )
                
                    logger.debug(event_dict)
                else:
                    return render(request, 'error.html', { 'message': "Could not get the event. Is it private?" })

                # Handle events without ending time.
                if not 'end_time' in event_dict: 
                    event_dict['end_time'] = event_dict['start_time']

                logger.debug("Creating happening")                    

                he = HappeningEvent(title=event_dict['name'], 
                                    start_date=event_dict['start_time'],
                                    end_date=event_dict['end_time'],
                                    description=event_dict['description'],
                                    created_by=User.objects.get(pk=1), )

                logger.debug("Saving happening")                    

                he.save()

                place_name = None
                city = None
                street = None
                address_line_1 = ""
                address_line_2 = ""

                if 'place' in event_dict:
                    place_name = event_dict.get('place')['name']
                else:
                    raise
      
                if 'city' in event_dict.get('place', {}).get('location', {}):
                    city = event_dict.get('place', {}).get('location', {}).get('city')
                    
                if 'street' in event_dict.get('place', {}).get('location', {}):
                    street = event_dict.get('place', {}).get('location', {}).get('street')
                    address_line_1=event_dict['place']['location']['city']
                    address_line_2=street

                
                l = HappeningLocation.objects.create(name=place_name,
                                                     address_line_1=address_line_1,
                                                     address_line_2=address_line_2)


                # Att the location to the happening event.
                he.location.add(l)
            
                # Create the record of the event with the image url
               
                FacebookEvent.objects.create( event=he, facebook_event_id=eid , facebook_cover_image_url=event_pic['cover']['source'])
                
                success = True
            #Not a POST call, present the form to be filled in
            else:
                form = FaceBookEventForm()

    # HANDLE FAILURES
    except IntegrityError as ie:
        return render(request, "error.html", {"message":  "Eventet redan inlagt."})
    except User.DoesNotExist:
        logger.error("User missing, is admin registered in django?")
    except Exception as e:
        logger.error("When trying to add facebook event")
        return render(request, "error.html", {"message":  str(e)})
# SUCCESS
    if success:
        logger.info("Added facebook event: {}".format(str(eid)))
        return redirect('home')
    else:
        logger.info("Failed to add facebook event from form")
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
