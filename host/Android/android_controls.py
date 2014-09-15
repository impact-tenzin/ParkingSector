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
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from client.models import Client, BookedSpots
from user.models import RegularUser, LicencePlates, UserProfile
from FindParking.models import ParkingMarker, PriceList
from Android.bug_report import android_error
import re
from Android.models import MobileSession
from user.views import push_booking_request_to_parkingadmin, get_price_list_as_string
from user.email_confirmation import send_confirmation_email, send_account_activation_email, send_email_with_token_to_reset_password, send_email_after_fbregister
import random
import string

import pusher
from django.conf import settings
pusher.app_id = settings.PUSHER_APP_ID
pusher.key = settings.PUSHER_KEY
pusher.secret = settings.PUSHER_SECRET

p = pusher.Pusher()

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
        if user_is_logged_in(request.GET['session_key']):
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
            return HttpResponse("session_key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

# url: android_ajaxCall/lat/lng, reqeust: GET, response:json
# returns parkings around a point(lat, lng), example url: "android_ajaxCall/23.23232/42.254235"
def ajax_call(request, latlng):
    if 'android' in mobile(request):
        if user_is_logged_in(request.GET['session_key']):
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
            return HttpResponse("session_key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

# url: android_loginUser, request:POST, response: text/html
@csrf_exempt
def login_request(request):
    if 'android' in mobile(request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                #user.backend = 'django.contrib.auth.backends.ModelBackend'
                #login(request, user)
                session_key = create_and_begin_session(user)
                return HttpResponse(session_key, content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("User is None", content_type="text/html; charset=utf-8")
        except:
            return HttpResponse("User does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def create_and_begin_session(user):
    session_key = str(''.join(random.choice(string.ascii_letters + string.digits) for i in range(25)))
    session = MobileSession.objects.create(user=user, session_key=session_key)
    session.save()
    return session_key

def end_and_delete_session(session_key):
    session = MobileSession.objects.get(session_key=session_key)
    session.delete()

def user_is_logged_in(session_key):
    try:
        MobileSession.objects.get(session_key=str(session_key))
        android_error(1)
        return True
    except:
        return False

def get_user_by_sessionkey(session_key):
    try:
        user_id = MobileSession.objects.get(session_key=session_key).user_id
        user = User.objects.get(pk=user_id)
        return user
    except MobileSession.DoesNotExist:
        android_error(2)
    except User.DoesNotExist:
        android_error(3)

@csrf_exempt
def login_req(request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                #user.backend = 'django.contrib.auth.backends.ModelBackend'
                #login(request, user)
                session_key = create_and_begin_session(user)
                return HttpResponse(session_key, content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("User is None", content_type="text/html; charset=utf-8")
        except:
            return HttpResponse("User does not exist", content_type="text/html; charset=utf-8")

# url: android_logoutUser, request:POST, response: text/html
@csrf_exempt   
def logout_request(request):
    if 'android' in mobile(request):
        end_and_delete_session(request.POST['session_key'])
        return HttpResponse("logged out", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

@csrf_exempt
def logout_req(request):
    end_and_delete_session(request.POST['session_key'])
    return HttpResponse("logged out", content_type="text/html; charset=utf-8")

@csrf_exempt
def same(request):
    return HttpResponse(request.POST['session_key'], content_type="text/html; charset=utf-8")

#url: android_confirmBooking, request: POST, response: "Booking complete" if correct input
@csrf_exempt
def confirm_booking(request):
    #if 'android' in mobile(request):      
        if user_is_logged_in(request.POST['session_key']):
            try:
                user = get_user_by_sessionkey(request.POST['session_key'])
                RegularUser.objects.get(user=user.id)
            except RegularUser.DoesNotExist:
                android_error(4)
                return HttpResponse("RegularUser does not exist", content_type="text/html; charset=utf-8")
            if request.method == 'POST':
                user_bookedspots = BookedSpots.objects.filter(user_id=user.id, parking_id=request.POST['parking_id']).count()
                if user_bookedspots > 0:
                    return HttpResponse("already booked parkingspot here", content_type="text/html; charset=utf-8")
                parking_bookedspots = BookedSpots.objects.filter(parking_id=request.POST['parking_id']).count()
                try:
                    available_spaces = ParkingMarker.objects.get(id=request.POST['parking_id']).availableSpaces
                except ParkingMarker.DoesNotExist:
                    android_error(5)
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
                        android_error(6)
                        return HttpResponse("ParkingMarker does not exist", content_type="text/html; charset=utf-8")
                    except PriceList.DoesNotExist:
                        android_error(7)
                        return HttpResponse("PriceList does not exist", content_type="text/html; charset=utf-8")
                    arrival_time = request.POST['arrival_time']
                    duration = request.POST['duration']
                    licence_plate = request.POST['licence_plate']
                    user_id = user.id
                    booked = BookedSpots.objects.create(parking_id=parking_id, user_id=user_id,
                                                        parking_address=parking_address,
                                                        price_list=price_list, arrival_time=arrival_time,
                                                        duration=duration, licence_plate=licence_plate,
                                                        lat=lat,
                                                        lng=lng)
                    booked.save()
                    send_confirmation_email(user.id, booked)
                    push_booking_request_to_parkingadmin(parking_id, booked, 'add_request')
                    return HttpResponse("Booking completed", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
    #else:
        #return HttpResponse("Error", content_type="text/html; charset=utf-8")

#url: android_getBookingRequests, request: GET, response: json
@csrf_exempt
def get_booking_requests(request):
    if 'android' in mobile(request):
        if user_is_logged_in(request.GET['session_key']):
            user = get_user_by_sessionkey(request.GET['session_key'])
            booking_requests = BookedSpots.objects.filter(user_id=user.id)        
            data = serializers.serialize("json", booking_requests)
            return HttpResponse(data, content_type="application/json; charset=utf-8") 
        else:
            return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

#url: android_getLicencePlates, request: GET, response: json
@csrf_exempt
def get_licence_plates(request):
    if 'android' in mobile(request):
        if user_is_logged_in(request.GET['session_key']):
            user = get_user_by_sessionkey(request.GET['session_key'])
            licence_plates = LicencePlates.objects.filter(user_id=request.user.id)       
            data = serializers.serialize("json", licence_plates)
            return HttpResponse(data, content_type="application/json; charset=utf-8") 
        else:
            return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

#url: android_removeLicencePlate, request: POST, response: "deletion complete"
@csrf_exempt
def remove_licence_plate(request):
    if 'android' in mobile(request):
        if user_is_logged_in(request.POST['session_key']):
                plate_id = request.POST['plate_id']
                try:
                    LicencePlates.objects.get(id=plate_id).delete()
                except LicencePlates.DoesNotExist:
                    android_error(8)
                return HttpResponse("deletion complete", content_type="text/html; charset=utf-8")        
        else:
            return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

#url: android_cancelBooking, request: POST, response: "cancelation complete"    
@csrf_exempt
def cancel_booking(request):
    if 'android' in mobile(request):
        if user_is_logged_in(request.POST['session_key']):
                booking_id = request.POST["booking_id"]
                try:
                    booked = BookedSpots.objects.get(id=booking_id)
                    push_booking_request_to_parkingadmin(booked.parking_id, booked, 'delete_request')
                    booked.delete()
                    return HttpResponse("cancelation complete", content_type="text/html; charset=utf-8")
                except BookedSpots.DoesNotExist:
                    register_error(9)
                    return HttpResponse("BookedSpot does not exist", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")