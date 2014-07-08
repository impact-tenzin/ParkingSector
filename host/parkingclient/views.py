# -*- coding: utf-8 -*- 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from parkingclient.forms import LoginForm, RegistrationForm
from parkingclient.models import Client, RegularUser, ParkingHistory, BookedSpots, LicencePlates
from FindParking.models import ParkingMarker, PriceList
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from datetime import datetime

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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            reguser = authenticate(username=username, password=password)
            if reguser is not None:
                try:
                    RegularUser.objects.get(user=reguser.id)
                    login(request, reguser)
                    return HttpResponseRedirect('/findparking/')
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
            Client.objects.get(user=request.user.id)
            return render_to_response('clientprofile.html', {}, context_instance=RequestContext(request))
        except Client.DoesNotExist:
            pass
        
        try:           
            RegularUser.objects.get(user=request.user.id)
            return render_to_response('userprofile.html', {}, context_instance=RequestContext(request))
        except RegularUser.DoesNotExist:
            pass
        
        return HttpResponseRedirect('/admin')

def logout_request(request):
        logout(request)
        return HttpResponseRedirect('/')

def save_parking_info(request):
        """
        save the date duration and the pricelist of the person leaving the parking
        who has booked his place from ParkingSector platform
        """
        if request.is_ajax():
            if request.user.is_authenticated():
                if request.method == 'POST':
                    parking_id = request.POST['parkingId']
                    user_id = request.POST['userId']
                    licence_plate = request.POST['drivingLicence']
                    arrival_time = request.POST['arrivalTime']
                    duration = request.POST['duration']
                    price_list = request.POST['priceList']
                    
                    to_add = ParkingHistory.objects.create(parking_id=parking_id,
                                                           user_id=user_id,
                                                           licence_plate=licence_plate,
                                                           arrival_time=arrival_time,
                                                           duration=duration,
                                                           price_list=price_list
                                                           )
                    to_add.save()
                    return HttpResponse("Completed", content_type="text/html; charset=utf-8")
                else:
                    return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("user is not authenticated", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("Error", content_type="text/html; charset=utf-8") 
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


def get_parking_requests(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            try:
                parking_id = Client.objects.get(user=request.user.id).parking_id
            except Client.DoesNotExist:
                send_data()
                return HttpResponse("client does not exist", content_type="text/html; charset=utf-8")
            spots = BookedSpots.objects.filter(parking_id=parking_id)
            data = serializers.serialize("json", spots)
            return HttpResponse(data, content_type="application/json; charset=utf-8")
        else:
            return HttpResponse("Error", content_type="text/html; charset=utf-8")
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
                return HttpResponse("Not authenticated", content_type="text/html; charset=utf-8")
            if request.method == 'POST':
                user_bookedspots = BookedSpots.objects.filter(user_id=request.user.id, parking_id=request.POST['parking_id']).count()
                if user_bookedspots > 0:
                    return HttpResponse("already booked parkingspot here", content_type="text/html; charset=utf-8")
                else:
                    parking_id = request.POST['parking_id']
                    #price_list = request.POST['price_list']
                    price_list_id = ParkingMarker.objects.get(id=parking_id).priceList
                    price_list = PriceList.objects.get(id=price_list_id)
                    parking_address = ParkingMarker.objects.get(id=parking_id).address
                    arrival_time = request.POST['arrival_time']
                    duration = request.POST['duration']
                    licence_plate = request.POST['licence_plate']
                    user_id = request.user.id
                    BookedSpots.objects.create(parking_id=parking_id, user_id=user_id,
                                               parking_address=parking_address,
                                               price_list=price_list, arrival_time=arrival_time,
                                               duration=duration, licence_plate=licence_plate)
                    return HttpResponse("Booking completed", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("Not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def send_data():
    pass

@csrf_exempt 
def cancel_booking(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.method == "POST":
                booking_id = request.POST["booking_id"]
                try:
                    BookedSpots.objects.get(id=booking_id).delete()
                    return HttpResponse("deletion complete", content_type="text/html; charset=utf-8")
                except BookedSpots.DoesNotExist:
                    send_data()
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
                if validate_password(reg_form):
                    return render_unvalid_password(request, reg_form)           
                return create_regular_user(request, reg_form)
            return user_already_exists(request, reg_form)
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
                                    password=reg_form.cleaned_data['password'])
    user.save()
              
    regular_user = RegularUser(user=user)
    regular_user.save()
                
    return HttpResponseRedirect('/login/user')

def user_already_exists(request, reg_form):
    context = {
               'form': reg_form,
               'msg':'Това потребителско име вече съществува. Моля, изберете друго!'
            }
    return render_to_response('registration.html', context, context_instance=RequestContext(request))

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

@csrf_exempt 
def actualise_price_list(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.method == 'POST':
                
                one_hour = request.POST.get('one_hour', False)
                two_hour = request.POST.get('two_hour', False)
                three_hour = request.POST.get('three_hour', False)
                four_hour = request.POST.get('four_hour', False)
                five_hour = request.POST.get('five_hour', False)
                six_hour = request.POST.get('six_hour', False)
                seven_hour = request.POST.get('seven_hour', False)
                eight_hour = request.POST.get('eight_hour', False)
                nine_hour = request.POST.get('nine_hour', False)
                ten_hour = request.POST.get('ten_hour', False)
                elven_hour = request.POST.get('eleven_hour', False)
                twelve_hour = request.POST.get('twelve_hour', False)
                
                try:
                    parking_id = Client.objects.get(user=request.user.id).parking_id
                except Client.DoesNotExist:
                    send_data()
                
                try:
                    price_list_id = ParkingMarker.objects.get(id=parking_id).priceList_id
                except ParkingMarker.DoesNotExist:
                    send_data()
                
                 
                PriceList.objects.filter(id=price_list_id).update(
                                                                oneHour = one_hour,
                                                                twoHours = two_hour,
                                                                threeHours = three_hour,
                                                                fourHours = four_hour,
                                                                fiveHours = five_hour,
                                                                sixHours = six_hour,
                                                                sevenHours = seven_hour,
                                                                eightHours = eight_hour,
                                                                nineHours = nine_hour,
                                                                tenHours = ten_hour,
                                                                elevenHours = elven_hour,
                                                                twelveHours = twelve_hour
                                                           )
                return HttpResponse("actualisation complete", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
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
                    send_data()
                return HttpResponse("deletion complete", content_type="text/html; charset=utf-8")        
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")
    
def get_price_list(request):
    if request.is_ajax():
        if request.method == "GET":
            if request.user.is_authenticated():
                try:
                    parking_id = Client.objects.get(user=request.user.id).parking_id
                    price_list_id = ParkingMarker.objects.get(id=parking_id).priceList_id
                    price_list = PriceList.objects.filter(id=price_list_id)
                    data = serializers.serialize("json", price_list)
                    return HttpResponse(data, content_type="application/json; charset=utf-8")
                except Client.DoesNotExist:
                    send_data()
                    return HttpResponse("Error on getting pricelist", content_type="text/html; charset=utf-8")
                except ParkingMarker.DoesNotExist:
                    send_data()
                    return HttpResponse("Error on getting pricelist", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

@login_required   
def render_price_list_page(request):
        return render_to_response('cena-chas.html', {}, context_instance=RequestContext(request))
    