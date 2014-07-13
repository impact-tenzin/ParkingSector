# -*- coding: utf-8 -*- 
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from home.forms import LocationForm, SubscribeForm
from FindParking.models import ParkingMarker, ParkingFeatures, PaymentMethod
from home.models import Viewer, Statistics, Locations
from django.db import IntegrityError
import math
import threading

customers = int(Statistics.objects.get(name__exact='customers').stat)

def home(request):  
    """
    function that take a request from the website
    and if request is GET then returns html with a form containing base values for 
    some fields: fromHour, toHour, fromPeriod, toPeriod;
    if POST then takes the latitude and longitude coordinates of the address that the user has written
    as well as the address, then make SQL requests for near parkings and their features
    finally returns html with selected parkings 
    """
    if request.method == 'GET':
        return home_view(request)
    else:
        if 'subsribeForm' in request.POST:
            return handle_subscribe_request(request)
        elif 'addressForm' in request.POST:     
            return redirect_to_map_from_searchbar(request)

def home_view(request):
    subscribe_form = SubscribeForm()
    address_form = LocationForm()
    fast_choice_locations = Locations.objects.all()
    context = {
               'addressForm':address_form,
               'subscribeForm':subscribe_form,
               "counter":customers,
               "locations":fast_choice_locations,
               }
    return render_to_response('index.html', context, context_instance=RequestContext(request))

def handle_subscibe_request(request):
    subscribe_form = SubscribeForm(request.POST)
    address_form = LocationForm()
    try:
        if subscribe_form.is_valid():
            email = subscribe_form.cleaned_data['email']
            name = subscribe_form.cleaned_data['name']
            to_add = Viewer.objects.create(email=email, name=name)
            to_add.save()
            context = {
                       'msg':'thanks',
                       'form':'subscribeForm',
                       'addressForm':address_form,
                       'subscribeForm':subscribe_form,
                       "counter":customers
                       }
            return render_to_response('index.html', context, context_instance=RequestContext(request))
        context = {
                   'msg':'notValid',
                   'form':'subscribeForm',
                   'addressForm':address_form,
                   'subscribeForm':subscribe_form,
                   "counter":customers,
                   }
        return render_to_response('index.html', context, context_instance=RequestContext(request))
    except IntegrityError:
        context = {
                   'msg':'existing',
                   'form':'subscribeForm',
                   'addressForm':address_form,
                   'subscribeForm':subscribe_form,
                   "counter":customers
                   }
        return render_to_response('index.html', context, context_instance=RequestContext(request))

def redirect_to_map_from_searchbar(request):
    subscribe_form = SubscribeForm()
    address_form = LocationForm(request.POST)
    if address_form.is_valid():
        lat_address = address_form.cleaned_data['lat']
        lng_address = address_form.cleaned_data['lng']
        address = address_form.cleaned_data['address']
        if address == '':
            increase_aroundme_stat()
        context = {
                   'address':address,
                    'geolocate':'true',
                    'lat':lat_address,
                    'lng':lng_address,
                    }
        return render_to_response('findparking.html', context , context_instance=RequestContext(request))
    else:
        parkings = ParkingMarker.objects.all()  # has to take parkings for homepage
        cnotext = {
                   'addressForm':address_form,
                   'subscribeForm':subscribe_form,
                    }
        return render_to_response('index.html', context, context_instance=RequestContext(request))

def increase_aroundme_stat():
    around_me_stat = int(Statistics.objects.get(name__exact='findAroundMe').stat)
    around_me_stat = around_me_stat + 1
    Statistics.objects.filter(name__exact='findAroundMe').update(stat=around_me_stat)
        
def distance(origin, destination):
    """
    function that calculates and returns the distance between two points
    where each point has two values - latitude and longitude
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def increase_customer(request):
    global customers
    if request.is_ajax():
        customers = int(Statistics.objects.get(name__exact='customers').stat)
        customers = customers + 1
        Statistics.objects.filter(name__exact='customers').update(stat=customers)
        return HttpResponse(str(customers) + "- +1 ", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def is_logged_in(request):
    if request.is_ajax():
        if not request.user.is_authenticated():
            return HttpResponse("NotAuthenticated", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("Authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def home_booking(request):
    if request.is_ajax():
        current_counter = int(Statistics.objects.get(name__exact='homeBooking').stat)
        current_counter = current_counter + 1
        Statistics.objects.filter(name__exact='homeBooking').update(stat=current_counter)
        return HttpResponse("Completed", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def increase():
    customers = int(Statistics.objects.get(name__exact='customers').stat)
    customers = customers + 1
    Statistics.objects.filter(name__exact='customers').update(stat=customers)
  
def redirect_to_map(request, latlng):
    lat = float(latlng.split('/')[0])
    lng = float(latlng.split('/')[1])
    context = {
                    'geolocate':'true',
                    'lat':lat,
                    'lng':lng,
                    }
    return render_to_response('findparking.html', context , context_instance=RequestContext(request))