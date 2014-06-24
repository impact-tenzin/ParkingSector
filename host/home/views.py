# -*- coding: utf-8 -*- 
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from home.forms import LocationForm, SubscribeForm
from FindParking.models import ParkingMarker, ParkingFeatures, PaymentMethod
from home.models import Viewer, Statistics
from django.db import IntegrityError
import math
import threading
from parkingclient.decorators import json_view

customers = int(Statistics.objects.get(name__exact='customers').stat)

@json_view
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
            try:
                subscribe_form = SubscribeForm(request.POST);
                address_form = LocationForm()
                if subscribe_form.is_valid():
                    email = subscribe_form.cleaned_data['email']
                    name = subscribe_form.cleaned_data['name']
                    to_add = Viewer.objects.create(email = email, name = name)
                    to_add.save()
                    context = {'msg':'thanks','form':'subscribeForm', 'addressForm':address_form,'subscribeForm':subscribe_form,"counter":customers}
                    return render_to_response('index.html', context, context_instance=RequestContext(request))
                context = {'msg':'notValid','form':'subscribeForm', 'addressForm':address_form,'subscribeForm':subscribe_form,"counter":customers}
                return render_to_response('index.html', context, context_instance=RequestContext(request))
            except IntegrityError:
                context = {'msg':'existing','form':'subscribeForm','addressForm':address_form,'subscribeForm':subscribe_form,"counter":customers}
                return render_to_response('index.html', context, context_instance=RequestContext(request))
        elif 'addressForm' in request.POST:     
            subscribe_form = SubscribeForm();   
            address_form = LocationForm(request.POST)
            if address_form.is_valid():
                latAddress = address_form.cleaned_data['lat']
                lngAddress = address_form.cleaned_data['lng']
                address = address_form.cleaned_data['address']
                if address == '':
                    increaseAroundMeStat()
                #parkings = [parking for parking in ParkingMarker.objects.all() if distance([parking.lat, parking.lng], [latAddress, lngAddress]) < 1]
                #features = [ParkingFeatures.objects.get(id=parking.features_id) for parking in parkings]
                #payment_methods = [PaymentMethod.objects.get(id=parking.paymentMethod_id) for parking in parkings];
                context = {'address':address,'geolocate':'true','lat':latAddress, 'lng':lngAddress,}
                return render_to_response('findparking.html', context , context_instance=RequestContext(request))
            else:
                parkings = ParkingMarker.objects.all();#has to take parkings for homepage
                return render_to_response('index.html', {'addressForm':address_form,'subscribeForm':subscribe_form,} , context_instance=RequestContext(request))

def home_view(request):
    subscribe_form = SubscribeForm()
    address_form = LocationForm()
    context = {'addressForm':address_form,'subscribeForm':subscribe_form,"counter":customers,}
    return render_to_response('index.html', context, context_instance=RequestContext(request))

def increaseAroundMeStat():
    aroundMeStat = int(Statistics.objects.get(name__exact='findAroundMe').stat)
    aroundMeStat = aroundMeStat + 1
    Statistics.objects.filter(name__exact='findAroundMe').update(stat=aroundMeStat)
        
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

def increaseCustomer(request):
    global customers
    if request.is_ajax():
        customers = int(Statistics.objects.get(name__exact='customers').stat)
        customers = customers + 1
        Statistics.objects.filter(name__exact='customers').update(stat=customers)
        return HttpResponse(str(customers)+"- +1 ", content_type="text/html; charset=utf-8")
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

def homeBooking(request):
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
  
