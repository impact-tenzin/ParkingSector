# -*- coding: utf-8 -*- 

from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from FindParking.models import ParkingMarker, ParkingFeatures, PaymentMethod, PriceList
from home.views import distance
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from home.models import Viewer
from django.contrib.auth.models import User
from django.core import serializers
from itertools import chain
import re

def mobile(request):

    device = {}

    ua = request.META.get('HTTP_USER_AGENT', '').lower()

    if ua.find("iphone") > 0:
        device['iphone'] = "iphone" + re.search("iphone os (\d)", ua).groups(0)[0]

    if ua.find("ipad") > 0:
        device['ipad'] = "ipad"

    if ua.find("android") > 0:
        device['android'] = "android" + re.search("android (\d\.\d)", ua).groups(0)[0].translate(None, '.')

    # spits out device names for CSS targeting, to be applied to <html> or <body>.
    device['classes'] = " ".join(v for (k,v) in device.items())

    return device


# url: android_sofiaParkings, reqeust: GET, response:json
def sofia_parkings(request):
    if 'android' in mobile(request):
        parkings = ParkingMarker.objects.filter(city__exact='София')
            
        features = [ParkingFeatures.objects.get(id=parking.features_id)
                    for parking in parkings
        ]
    
        payment_methods = [PaymentMethod.objects.get(id=parking.paymentMethod_id)
                               for parking in parkings
        ]
            
        price_lists = [PriceList.objects.get(id=parking.priceList_id)
                           for parking in parkings
        ]
    
        combined = list(chain(parkings, payment_methods, features, price_lists))
        data = serializers.serialize("json", combined)
        return HttpResponse(data, content_type="application/json; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

# url: android_ajaxCall/lat/lng, reqeust: GET, response:json
# returns parkings around a point(lat, lng), example url: "android_ajaxCall/23.23232/42.254235"
def ajax_call(request, latlng):
    if 'android' in mobile(request):
        lat = float(latlng.split('/')[0])
    
        lng = float(latlng.split('/')[1])
            
        parkings = [parking
                for parking in ParkingMarker.objects.all()
                if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5
        ]
    
        methods = [PaymentMethod.objects.get(id=parking.paymentMethod_id)
                    for parking in ParkingMarker.objects.all() 
                    if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5
        ]
    
        features = [ParkingFeatures.objects.get(id=parking.features_id)
                    for parking in ParkingMarker.objects.all() 
                    if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5
        ]
            
        price_lists = [PriceList.objects.get(id=parking.priceList_id)
                       for parking in ParkingMarker.objects.all() 
                       if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5
        ]
            
        combined = list(chain(parkings, methods, features, price_lists))
        data = serializers.serialize("json", combined)
        return HttpResponse(data, content_type="application/json; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

# url: android_loginUser, request:POST, response: text/html
def login_request(request):
    if 'android' in mobile(request):
        username = reqeust.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username, password=password)
            if user is not None:
                reguser.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, reguser)
                return HttpResponse("login successful", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("User is None", content_type="text/html; charset=utf-8")
        except User.DoesNotExist:
            return HttpResponse("User does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")
#tova par4e kod sohte ne e prigodena kato android kontrola, no go razgledai, to e za zapzvane na mqsto na parkings
"""
@csrf_exempt
def confirm_booking(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            try:           
                RegularUser.objects.get(user=request.user.id)
            except RegularUser.DoesNotExist:
                register_error(3)
                return HttpResponse("Not authenticated", content_type="text/html; charset=utf-8")
            if request.method == 'POST':
                user_bookedspots = BookedSpots.objects.filter(user_id=request.user.id, parking_id=request.POST['parking_id']).count()
                if user_bookedspots > 0:
                    return HttpResponse("already booked parkingspot here", content_type="text/html; charset=utf-8")
                parking_bookedspots = BookedSpots.objects.filter(parking_id=request.POST['parking_id']).count()
                try:
                    available_spaces = ParkingMarker.objects.get(id=request.POST['parking_id']).availableSpaces
                except ParkingMarker.DoesNotExist:
                    register_error(4)
                    return HttpResponse("ParkingMarker does not exist", content_type="text/html; charset=utf-8")
                if parking_bookedspots >= available_spaces:
                    return HttpResponse("all spaces are taken", content_type="text/html; charset=utf-8")
                else:
                    parking_id = request.POST['parking_id']
                    try:
                        parking = ParkingMarker.objects.get(id=parking_id)
                        parking_address = parking.address
                        lat = parking.lat
                        lng = parking.lng
                        price_list_id = parking.priceList_id
                        price_list = get_price_list_as_string(PriceList.objects.get(id=price_list_id))
                    except ParkingMarker.DoesNotExist:
                        register_error(5)
                        return HttpResponse("ParkingMarker does not exist", content_type="text/html; charset=utf-8")
                    except PriceList.DoesNotExist:
                        register_error(6)
                        return HttpResponse("PriceList does not exist", content_type="text/html; charset=utf-8")
                    arrival_time = request.POST['arrival_time']
                    duration = request.POST['duration']
                    licence_plate = request.POST['licence_plate']
                    user_id = request.user.id
                    booked = BookedSpots.objects.create(parking_id=parking_id, user_id=user_id,
                                                        parking_address=parking_address,
                                                        price_list=price_list, arrival_time=arrival_time,
                                                        duration=duration, licence_plate=licence_plate,
                                                        lat=lat,
                                                        lng=lng)
                    booked.save()
                    send_confirmation_email(request.user.id, booked)
                    push_booking_request_to_parkingadmin(parking_id, booked, 'add_request')
                    return HttpResponse("Booking completed", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("Not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")    

def push_booking_request_to_parkingadmin(parking_id, booked, type):
    data = serializers.serialize("json", [booked])
    channel = 'parking_admin_id-' + str(parking_id)
    if type == 'add_request':
        p[channel].trigger('message', {
                'booking_request': data,
                'message': 'add_request'
        },)
    else:
        p[channel].trigger('message', {
                'booking_request': data,
                'message': 'delete_request'
        },)
"""