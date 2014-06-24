from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from parkingclient.forms import LoginForm
from parkingclient.models import Client, RegularUser, ParkingHistory, BookedSpots, LicencePlates
from FindParking.models import ParkingMarker
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

def LoginRequest(request, type):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/profile/')
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if type == "user":
                    if form.is_valid():
                            username = form.cleaned_data['username']
                            password = form.cleaned_data['password']
                            reguser = authenticate(username=username, password=password)
                            if reguser is not None:
                                try:
                                    RegularUser.objects.get(user = reguser.id)
                                    login(request, reguser)
                                    return HttpResponseRedirect('/findparking/')
                                except RegularUser.DoesNotExist:
                                    return render_to_response('loginuser.html', {'form': form}, context_instance=RequestContext(request))
                            else:
                                    return render_to_response('loginuser.html', {'form': form}, context_instance=RequestContext(request))
                    else:
                            return render_to_response('loginuser.html', {'form': form}, context_instance=RequestContext(request))
                else:
                    if form.is_valid():
                            username = form.cleaned_data['username']
                            password = form.cleaned_data['password']
                            client = authenticate(username=username, password=password)
                            if client is not None:
                                try:
                                    Client.objects.get(user = client.id)
                                    login(request, client)
                                    return HttpResponseRedirect('/profile/')
                                except Client.DoesNotExist:
                                    return render_to_response('loginclient.html', {'form': form}, context_instance=RequestContext(request))
                            else:
                                    return render_to_response('loginclient.html', {'form': form}, context_instance=RequestContext(request))
                    else:
                            return render_to_response('loginclient.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show the login form '''
                if type == "user":
                    form = LoginForm()
                    context = {'form': form}
                    return render_to_response('loginuser.html', context, context_instance=RequestContext(request))
                else:
                    form = LoginForm()
                    context = {'form': form}
                    return render_to_response('loginclient.html', context, context_instance=RequestContext(request))

@login_required
def Profile(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        #client = request.user.get_profile
        try:
            client = Client.objects.get(user = request.user.id)
            context = {'client': client}
            return render_to_response('clientprofile.html', context, context_instance=RequestContext(request))
        except Client.DoesNotExist:
            pass
        
        try:           
            reguser = RegularUser.objects.get(user = request.user.id)
            context = {'user': reguser}
            return render_to_response('userprofile.html', context, context_instance=RequestContext(request))
        except RegularUser.DoesNotExist:
            pass
        
        return HttpResponseRedirect('/admin')

def LogoutRequest(request):
        logout(request)
        return HttpResponseRedirect('/')

def SaveParkingInfo(request):
        """
        save the date duration and the pricelist of the person leaving the parking
        who has booked his place from ParkingSector platform
        """
        if request.is_ajax():
            if request.method == 'POST':
                parking_id = request.POST['parkingId']
                licence_plate = request.POST['drivingLicence']
                arrival_time = request.POST['arrivalTime']
                duration = request.POST['duration']
                price_list = request.POST['priceList']
                
                to_add = ParkingHistory.objects.create(parking_id=parking_id, licence_plate=licence_plate, arrival_time=arrival_time, duration=duration, price_list=price_list)
                to_add.save()
                return HttpResponse("Completed", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
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
def SignInBeforeBooking(request):
    if request.is_ajax():
        username = request.POST['name']
        password = request.POST['pass']
        reguser = authenticate(username=username, password=password)
        if reguser is not None:
            try:
                RegularUser.objects.get(user = reguser.id)
                login(request, reguser)
                return HttpResponse("Login Successful", content_type="text/html; charset=utf-8")
            except RegularUser.DoesNotExist:
                return HttpResponse("User does not exist", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("Cant authenticate", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")


def GetParkingRequests(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            parking_id = Client.objects.get(user=request.user.id).parking_id
            spots = BookedSpots.objects.filter(parking_id=parking_id)
            data = serializers.serialize("json", spots)
            return HttpResponse(data, content_type="application/json; charset=utf-8")
        else:
            return HttpResponse("Error", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def BookParkingSpot(request):
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
def ConfirmBooking(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            try:           
                RegularUser.objects.get(user = request.user.id)
            except RegularUser.DoesNotExist:
                return HttpResponse("Not authenticated", content_type="text/html; charset=utf-8")
            if request.method == 'POST':
                user_bookedspots = BookedSpots.objects.filter(user_id=request.user.id, parking_id=request.POST['parking_id']).count()
                if user_bookedspots > 0:
                    return HttpResponse("already booked parkingspot here", content_type="text/html; charset=utf-8")
                else:
                    parking_id = request.POST['parking_id']
                    #price_list = request.POST['price_list']
                    price_list = ParkingMarker.objects.get(id=parking_id).pricePerHour
                    arrival_time = request.POST['arrival_time']
                    duration = request.POST['duration']
                    licence_plate = request.POST['licence_plate']
                    user_id = request.user.id
                    BookedSpots.objects.create(parking_id=parking_id, user_id=user_id,
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
  
def cancel_booking(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.method == "POST":
                booking_id = request.POST["booking_id"]
                try:
                    BookedSpots.objects.get(id=booking_id).delete()
                except BookedSpots.DoesNotExist:
                    send_data()
                    return HttpResponse("does not exist", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")