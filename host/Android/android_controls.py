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
from user.views import push_booking_request_to_parkingadmin, get_price_list_as_string, generate_activation_key
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
        
            #payment_methods = [PaymentMethod.objects.get(id=parking.paymentMethod_id)
            #                       for parking in parkings
            #]
                
            price_lists = [PriceList.objects.get(id=parking.priceList_id)
                               for parking in parkings
            ]
        
            #combined = list(chain(parkings, payment_methods, features, price_lists))
            combined = list(chain(parkings, features, price_lists))
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
        
            #methods = [PaymentMethod.objects.get(id=parking.paymentMethod_id)
            #            for parking in ParkingMarker.objects.all() 
            #            if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5
            #]
        
            features = [ParkingFeatures.objects.get(id=parking.features_id)
                        for parking in ParkingMarker.objects.all() 
                        if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5
            ]
                
            price_lists = [PriceList.objects.get(id=parking.priceList_id)
                           for parking in ParkingMarker.objects.all() 
                           if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5
            ]
                
            #combined = list(chain(parkings, methods, features, price_lists))
            combined = list(chain(parkings, features, price_lists))
            data = serializers.serialize("json", combined)
            return HttpResponse(data, content_type="application/json; charset=utf-8")
        else:
            return HttpResponse("session_key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def has_user_by_email(email):
    try:
        User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False

# url: android_loginUser, request:POST, response: text/html
@csrf_exempt
def login_request(request):
    if 'android' in mobile(request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            if has_user_by_email(username):
              username = User.objects.get(email=username).username
            user = authenticate(username=username, password=password)
            if user is not None:
                #user.backend = 'django.contrib.auth.backends.ModelBackend'
                #login(request, user)
                if user.is_active == True:
                    session_key = create_and_begin_session(user)
                    return HttpResponse(session_key, content_type="text/html; charset=utf-8")
                else:
                    return HttpResponse("unactivated account", content_type="text/html; charset=utf-8")
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
        return True
    except:
        android_error(1)
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

# url: android_logoutUser, request:POST, response: text/html
@csrf_exempt   
def logout_request(request):
    if 'android' in mobile(request):
        end_and_delete_session(request.POST['session_key'])
        return HttpResponse("logged out", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

#url: android_confirmBooking, request: POST, response: "Booking complete" if correct input
@csrf_exempt
def confirm_booking(request):
    if 'android' in mobile(request):      
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
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

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
            licence_plates = LicencePlates.objects.filter(user_id=user.id)       
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

#url: android_addLicencePlate, request: POST, response: "addition complete"
@csrf_exempt
def add_licence_plate(request):
    if 'android' in mobile(request):
        if user_is_logged_in(request.POST['session_key']):
                licence_plate = request.POST['licence_plate']
                user = get_user_by_sessionkey(request.POST['session_key'])
                try:
                    LicencePlates.objects.get(user_id=user.id, licence_plate=licence_plate)
                except LicencePlates.DoesNotExist:
                    LicencePlates.objects.create(user_id=user.id, licence_plate=licence_plate).save()
                    return HttpResponse("addition complete", content_type="text/html; charset=utf-8")
                return HttpResponse("already exists", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
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
                    android_error(9)
                    return HttpResponse("BookedSpot does not exist", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

#url: android_resetPassword, request: POST, response: "password reset successful"
@csrf_exempt
def reset_password(request):
    if 'android' in mobile(request):
        if user_is_logged_in(request.POST['session_key']):
            user = get_user_by_sessionkey(request.POST['session_key'])
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            return HttpResponse("password reset successful", content_type="text/html; charset=utf-8") 
        else:
            return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

#url: android_fblogin request: POST, response: "session_key"
@csrf_exempt
def facebook_login(request):
    if 'android' in mobile(request):
            email = request.POST['email']
            username = request.POST['username']
            try:
                reguser = User.objects.get(id=RegularUser.objects.get(fb_email=email).user_id)
            except RegularUser.DoesNotExist:
                try:
                    reguser = User.objects.get(email=email)
                except User.DoesNotExist:
                    return register_user_with_fb(email, username)
            if reguser is not None:
                #reguser.backend = 'django.contrib.auth.backends.ModelBackend'
                #login(request, reguser)
                session_key = create_and_begin_session(reguser)
                return HttpResponse(session_key, content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("Cant authenticate", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")
  
def register_user_with_fb(email, username):
    if not email_unique(email):
        return HttpResponse("email already exists", content_type="text/html; charset=utf-8")
    if not username_unique(username):
        return HttpResponse("username already exists", content_type="text/html; charset=utf-8")
    password = str(''.join(random.choice(string.ascii_letters + string.digits) for i in range(12)))
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password,
                                            )
    user.save()

    regular_user = RegularUser(user=user,
                                fb_email=email,
                                fb_name=username)
    regular_user.save()
            
    #user.backend = 'django.contrib.auth.backends.ModelBackend'
    #login(request, user)
    session_key = create_and_begin_session(user)
            
    send_email_after_fbregister(email)
            
    return HttpResponse(session_key, content_type="text/html; charset=utf-8")

def email_unique(email):
    try:
        User.objects.get(email=email)
        return False
    except User.DoesNotExist:
        return True

def username_unique(username):
    try:
        User.objects.get(username=username)
        return False
    except User.DoesNotExist:
        return True

#url: android_register request: POST, response: "registration complete" 
@csrf_exempt
def create_regular_user(request):
    user = User.objects.create_user(username=request.POST['username'],
                                    email=request.POST['email'],
                                    password=request.POST['password'],
                                    )
    user.is_active = False
    user.save()

    regular_user = RegularUser(user=user)
    regular_user.save()
    
    activation_key = generate_activation_key()
    user_profile = UserProfile.objects.create(user=user, activation_key=activation_key)
    user_profile.save()
    
    send_account_activation_email(request.POST['email'], activation_key, user.id)
    
    #reguser = authenticate(username=reg_form.cleaned_data['username'], password=reg_form.cleaned_data['password'])
    #login(request, reguser)
                
    return HttpResponse("registration complete", content_type="text/html; charset=utf-8")


#url: android_resetEmail request: POST, response: "verified email"
@csrf_exempt
def check_for_valid_email(request):
    if 'android' in mobile(request):
            email = request.POST["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                try:
                    #user = RegularUser.objects.get(fb_email=email).user
                    user = User.objects.get(id=RegularUser.objects.get(fb_email=email).user_id)
                except:
                    return HttpResponse("invalid email", content_type="text/html; charset=utf-8")
                
            activation_key = generate_activation_key()
            user_profile = UserProfile.objects.create(user=user, activation_key=activation_key)
            user_profile.save()
            send_email_with_token_to_reset_password(email, activation_key, user.id)
            return HttpResponse("verified email", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

#url: android_getUsername request: GET, response: user.username
@csrf_exempt
def get_username(request):
    if 'android' in mobile(request):
        if user_is_logged_in(request.GET['session_key']):
            user = get_user_by_sessionkey(request.GET['session_key'])
            username = RegularUser.objects.get(user=user).fb_name
            if username is not None and len(username) is not 0:
                return HttpResponse(str(username), content_type="text/html; charset=utf-8")
            else:
                return HttpResponse(str(user.username), content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")