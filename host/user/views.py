# -*- coding: utf-8 -*- 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from user.forms import LoginForm, RegistrationForm
from client.models import Client, BookedSpots
from user.models import RegularUser, LicencePlates, UserProfile
from FindParking.models import ParkingMarker, PriceList
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from client.errors_and_messages import register_error
from user.email_confirmation import send_confirmation_email, send_account_activation_email, send_email_with_token_to_reset_password, send_email_after_fbregister
from django.conf import settings
import pusher
import string
import random

pusher.app_id = settings.PUSHER_APP_ID
pusher.key = settings.PUSHER_KEY
pusher.secret = settings.PUSHER_SECRET

p = pusher.Pusher()

def login_request(request, type):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/profile/')
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if type == "user":
                return handle_login_user_request(request, form)
            else:
                return handle_login_client_request(request, form)
        else:
            ''' user is not submitting the form, show the login form '''
            return render_login_page(request, type)

def handle_login_user_request(request, form):
        if form.is_valid():
            #username = form.cleaned_data['username']
            #password = form.cleaned_data['password']
            username = request.POST['username']
            if has_user_by_email(username):
              username = User.objects.get(email=username).username  
            password = request.POST['password']
            reguser = authenticate(username=username, password=password)
            if reguser is not None:
                try:
                    RegularUser.objects.get(user=reguser.id)
                    login(request, reguser)
                    return HttpResponseRedirect('/profile/')
                except RegularUser.DoesNotExist:
                    return render_to_response('loginuser.html',
                                              {'form': form, 'msg':'Грешно потребителско име или парола'},
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('loginuser.html',
                                          {'form': form, 'msg':'Грешно потребителско име или парола'},
                                          context_instance=RequestContext(request))
        else:
            return render_to_response('loginuser.html',
                                      {'form': form},
                                      context_instance=RequestContext(request))

def facebook_login(request):
    if request.is_ajax():
        if request.method == "POST":
            email = request.POST['email']
            username = request.POST['username']
            fb_id = request.POST['fb_id']
            try:
                reguser = User.objects.get(id=RegularUser.objects.get(fb_email=email).user_id)
            except RegularUser.DoesNotExist:
                try:
                    reguser = User.objects.get(email=email)
                except User.DoesNotExist:
                    return register_user_with_fb(request, email, username, fb_id)
            if reguser is not None:
                add_fb_id_if_absent(reguser, fb_id)
                reguser.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, reguser)
                return HttpResponse("fblogin complete", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("Cant authenticate", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")  

def add_fb_id_if_absent(reguser, fb_id):
    user = RegularUser.objects.get(user=reguser)
    if len(user.fb_id) == 0:
        user.fb_id = fb_id
        user.save()

def facebook_sync(request):
    if request.is_ajax():
        if request.method == "POST":
            email = request.POST['email']
            username = request.POST['username']
            try:
                reguser = RegularUser.objects.get(user=request.user.id)
                if reguser.fb_email == "":
                    reguser.fb_email = email
                    reguser.fb_name = username
                    reguser.save() 
                    return HttpResponse("sync complete", content_type="text/html; charset=utf-8")
                else:
                    return HttpResponse("already synced", content_type="text/html; charset=utf-8")        
            except RegularUser.DoesNotExist:
                return HttpResponse("RegularUser does not exist", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8") 

def has_user_by_email(email):
    try:
        User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False

def handle_login_client_request(request, form):
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            client = authenticate(username=username, password=password)
            if client is not None:
                try:
                    Client.objects.get(user=client.id)
                    login(request, client)
                    return HttpResponseRedirect('/profile/')
                except Client.DoesNotExist:
                    return render_to_response('loginclient.html',
                                              {'form': form, 'msg':'Грешно потребителско име или парола'},
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('loginclient.html',
                                          {'form': form, 'msg':'Грешно потребителско име или парола'},
                                          context_instance=RequestContext(request))
        else:
            return render_to_response('loginclient.html',
                                      {'form': form},
                                      context_instance=RequestContext(request))

def render_login_page(request, type):
    if type == "user":
        form = LoginForm()
        context = {'form': form}
        return render_to_response('loginuser.html', context, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        context = {'form': form}
        return render_to_response('loginclient.html', context, context_instance=RequestContext(request))

@login_required
def profile(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/user')
        # client = request.user.get_profile
        try:
            parking_id = Client.objects.get(user=request.user.id).parking_id
            current_available_spaces = ParkingMarker.objects.get(id=parking_id).availableSpaces
            return render_to_response('clientprofile.html',
                                       {
                                        'available_spaces':current_available_spaces,
                                        'PUSHER_KEY': settings.PUSHER_KEY,
                                        'parking_id': parking_id
                                        },
                                        context_instance=RequestContext(request))
        except Client.DoesNotExist:
            pass
        except ParkingMarker.DoesNotExist:
            register_error(14)
        
        try:           
            RegularUser.objects.get(user=request.user.id)
            user = User.objects.get(id=request.user.id)
            if user.is_active == True:
                return render_to_response('userprofile.html', {}, context_instance=RequestContext(request))
            else:
                form = LoginForm(request.POST)
                return render_to_response('loginuser.html',
                                           {
                                            'msg': 'Акаунтът Ви не е активиран!',
                                            'form': form
                                            },
                                            context_instance=RequestContext(request))
        except RegularUser.DoesNotExist:
            pass
        
        return HttpResponseRedirect('/admin')

def logout_request(request):
        logout(request)
        return HttpResponseRedirect('/')

"""
def LeavingDriver(request):
    if request.is_ajax():
        parking_id = request.POST['id']
        available_spots = int(ParkingMarker.objects.get(id=parking_id).availableSpaces)
        available_spots = available_spots + 1
        ParkingMarker.objects.filter(id=parking_id).update(availableSpaces=available_spots)
        return HttpResponse("Completed", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def ArrivingDriver(request):
    if request.is_ajax():
        parking_id = request.POST['id']
        available_spots = int(ParkingMarker.objects.get(id=parking_id).availableSpaces)
        available_spots = available_spots - 1
        ParkingMarker.objects.filter(id=parking_id).update(availableSpaces=available_spots)
        return HttpResponse("Completed", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")
"""

@csrf_exempt 
def signin_before_booking(request):
    if request.is_ajax():
        if request.method == "POST":
            username = request.POST['name']
            password = request.POST['pass']
            reguser = authenticate(username=username, password=password)
            if reguser is not None:
                try:
                    RegularUser.objects.get(user=reguser.id)
                    login(request, reguser)
                    return HttpResponse("Login Successful", content_type="text/html; charset=utf-8")
                except RegularUser.DoesNotExist:
                    return HttpResponse("User does not exist", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("Cant authenticate", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def booking_parkingspot(request):
    if request.is_ajax():
        if not request.user.is_authenticated():
            return HttpResponse("Not authenticated", content_type="text/html; charset=utf-8")
        else:
            plates = LicencePlates.objects.filter(user_id=request.user.id)
            data = serializers.serialize("json", plates)
            return HttpResponse(data, content_type="application/json; charset=utf-8") 
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

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

def get_price_list_as_string(price_list):
    pices_as_string = str(price_list.oneHour) + ";" + str(price_list.oneHour) + ";" + str(price_list.twoHours) + ";" + str(price_list.threeHours) + ";" + str(price_list.fourHours) + ";" + str(price_list.fiveHours) + ";" + str(price_list.sixHours) + ";" + str(price_list.sevenHours) + ";" + str(price_list.eightHours) + ";" + str(price_list.nineHours) + ";" + str(price_list.tenHours) + ";" + str(price_list.elevenHours) + ";" + str(price_list.twelveHours)
    return pices_as_string

@csrf_exempt 
def cancel_booking(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.method == "POST":
                booking_id = request.POST["booking_id"]
                try:
                    booked = BookedSpots.objects.get(id=booking_id)
                    push_booking_request_to_parkingadmin(booked.parking_id, booked, 'delete_request')
                    booked.delete()
                    return HttpResponse("deletion complete", content_type="text/html; charset=utf-8")
                except BookedSpots.DoesNotExist:
                    register_error(7)
                    return HttpResponse("BookedSpot does not exist", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def register_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            try:
                User.objects.get(username=reg_form.cleaned_data['username'])
            except User.DoesNotExist:
                try:
                    User.objects.get(email=reg_form.cleaned_data['email'])
                except User.DoesNotExist:
                    try:
                        RegularUser.objects.get(fb_email=reg_form.cleaned_data['email'])
                    except RegularUser.DoesNotExist:
                        if validate_password(reg_form):
                            return render_unvalid_password(request, reg_form)           
                        return create_regular_user(request, reg_form)
                return user_already_exists(request, reg_form, "email_match")
            return user_already_exists(request, reg_form, "name_match")
        else:
            context = {
                       'form': reg_form,
                       'msg': 'Невалидна форма! Моля, попълнете всички полета!'                    
                       }
            return render_to_response('registration.html', context, context_instance=RequestContext(request))
    else:
        reg_form = RegistrationForm()
        context = {'form': reg_form}
        return render_to_response('registration.html', context, context_instance=RequestContext(request))

def validate_password(reg_form):
    return reg_form.cleaned_data['password'] != reg_form.cleaned_data['password1']

def render_unvalid_password(request, reg_form):
    context = {
               'form': reg_form,
               'msg':'Грешна парола!'
            }
    return render_to_response('registration.html', context, context_instance=RequestContext(request))

def create_regular_user(request, reg_form):
    user = User.objects.create_user(username=reg_form.cleaned_data['username'],
                                    email=reg_form.cleaned_data['email'],
                                    password=reg_form.cleaned_data['password'],
                                    )
    user.is_active = False
    user.save()

    regular_user = RegularUser(user=user)
    regular_user.save()
    
    activation_key = generate_activation_key()
    user_profile = UserProfile.objects.create(user=user, activation_key=activation_key)
    user_profile.save()
    
    send_account_activation_email(reg_form.cleaned_data['email'], activation_key, user.id)
    
    #reguser = authenticate(username=reg_form.cleaned_data['username'], password=reg_form.cleaned_data['password'])
    #login(request, reguser)
                
    regform = RegistrationForm()
    context = {
               'form': regform,
               'registration': 'successful',
               'email': reg_form.cleaned_data['email']
               }
    return render_to_response('registration.html', context, context_instance=RequestContext(request))

def register_user_with_fb(request, email, username, fb_id):
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
                                fb_name=username,
                                fb_id=fb_id)
    regular_user.save()
            
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
            
    send_email_after_fbregister(email)
            
    return HttpResponse("registration with fb complete", content_type="text/html; charset=utf-8")

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

def user_already_exists(request, reg_form, match):
    if match == "name_match":
        context = {
                   'form': reg_form,
                   'msg':'Това потребителско име вече съществува. Моля, изберете друго!'
                }
        return render_to_response('registration.html', context, context_instance=RequestContext(request))
    else:
        context = {
                   'form': reg_form,
                   'msg':'Този имейл вече съществува. Моля, изберете друг!'
                }
        return render_to_response('registration.html', context, context_instance=RequestContext(request))

def generate_activation_key():
    key = str(''.join(random.choice(string.ascii_letters + string.digits) for i in range(25)))
    return key   

def get_booking_requests(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            booking_requests = BookedSpots.objects.filter(user_id=request.user.id)
            licence_plates = LicencePlates.objects.filter(user_id=request.user.id)          
            combined = list(chain(booking_requests, licence_plates))
            data = serializers.serialize("json", combined)
            return HttpResponse(data, content_type="application/json; charset=utf-8") 
        else:
            return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def add_licence_plate(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.method == "POST":
                licence_plate = request.POST['licence_plate']
                try:
                    LicencePlates.objects.get(user_id=request.user.id, licence_plate=licence_plate)
                except LicencePlates.DoesNotExist:
                    LicencePlates.objects.create(user_id=request.user.id, licence_plate=licence_plate).save()
                    return HttpResponse("addition complete", content_type="text/html; charset=utf-8")
                return HttpResponse("already exists", content_type="text/html; charset=utf-8")      
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def remove_licence_plate(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.method == "POST":
                plate_id = request.POST['plate_id']
                try:
                    LicencePlates.objects.get(id=plate_id).delete()
                except LicencePlates.DoesNotExist:
                    register_error(10)
                return HttpResponse("deletion complete", content_type="text/html; charset=utf-8")        
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")
    
def display_error_page(request):
    return render_to_response('error_page.html', {}, context_instance=RequestContext(request))

def render_password_reset_form(request):
    return render_to_response(
                              'newpass_mail.html', {}, context_instance=RequestContext(request)
                              )

def check_for_valid_email(request):
    if request.is_ajax():
        if request.method == "POST":
            email = request.POST["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                try:
                    user = RegularUser.objects.get(fb_email=email).user
                except RegularUser.DoesNotExist:
                    return HttpResponse("invalid email", content_type="text/html; charset=utf-8")
                
            activation_key = generate_activation_key()
            user_profile = UserProfile.objects.create(user=user, activation_key=activation_key)
            user_profile.save()
            send_email_with_token_to_reset_password(email, activation_key, user.id)
            return HttpResponse("verified email", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def password_reset(request, activation_key, user_id):
    try:
       profile = UserProfile.objects.get(activation_key=activation_key)
    except UserProfile.DoesNotExist:
        return render_to_response('invalid_key.html', {}, context_instance=RequestContext(request))
    profile.delete()
    return render_to_response(
                              'newpass.html', {"user_id":user_id}, context_instance=RequestContext(request)
                              )

def get_fb_id(request):
    fb_id = RegularUser.objects.get(user=request.user.id).fb_id
    return HttpResponse(fb_id, content_type="text/html; charset=utf-8")