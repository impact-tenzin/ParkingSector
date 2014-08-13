# -*- coding: utf-8 -*- 
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from client.models import Client, ParkingHistory, BookedSpots
from FindParking.models import ParkingMarker, PriceList
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from client.errors_and_messages import register_error

@csrf_exempt 
def save_parking_info(request):
        """
        save the date duration and the pricelist of the person leaving the parking
        who has booked his place from ParkingSector platform
        """
        if request.is_ajax():
            if request.user.is_authenticated():
                if request.method == 'POST':
                    try:
                        spot = BookedSpots.objects.get(id=request.POST['booking_id'])
                    except BookedSpots.DoesNotExist:
                        register_error(1)
                        return HttpResponse("BookedSpot does not exist", content_type="text/html; charset=utf-8")
                    spot.is_parked = True
                    spot.save()
                    user_id = spot.user_id
                    licence_plate = spot.licence_plate
                    arrival_time = spot.arrival_time
                    duration = spot.duration
                    price_list = spot.price_list
                    parking_id = spot.parking_id
                    
                    try:
                        ParkingHistory.objects.get(parking_id=parking_id,
                                                           user_id=user_id,
                                                           licence_plate=licence_plate,
                                                           arrival_time=arrival_time,
                                                           duration=duration,
                                                           price_list=price_list
                                                           )
                    except:
                        to_add = ParkingHistory.objects.create(parking_id=parking_id,
                                                               user_id=user_id,
                                                               licence_plate=licence_plate,
                                                               arrival_time=arrival_time,
                                                               duration=duration,
                                                               price_list=price_list
                                                               )
                        to_add.save()
                        return HttpResponse("Completed", content_type="text/html; charset=utf-8")
                    return HttpResponse("this booking already exists in parking history", content_type="text/html; charset=utf-8")
                else:
                    return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("user is not authenticated", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("Error", content_type="text/html; charset=utf-8") 

@csrf_exempt 
def cancel_booking_admin(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.method == "POST":
                booking_id = request.POST["booking_id"]
                try:
                    BookedSpots.objects.get(id=booking_id).delete()
                    return HttpResponse("deletion complete", content_type="text/html; charset=utf-8")
                except BookedSpots.DoesNotExist:
                    register_error(15)
                    return HttpResponse("BookedSpot does not exist", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def get_parking_requests(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            try:
                parking_id = Client.objects.get(user=request.user.id).parking_id
            except Client.DoesNotExist:
                register_error(2)
                return HttpResponse("client does not exist", content_type="text/html; charset=utf-8")
            spots = BookedSpots.objects.filter(parking_id=parking_id)
            data = serializers.serialize("json", spots)
            return HttpResponse(data, content_type="application/json; charset=utf-8")
        else:
            return HttpResponse("Error", content_type="text/html; charset=utf-8")
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
                    register_error(8)
                
                try:
                    price_list_id = ParkingMarker.objects.get(id=parking_id).priceList_id
                except ParkingMarker.DoesNotExist:
                    register_error(9)
                
                 
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
                    register_error(11)
                    return HttpResponse("Error on getting pricelist", content_type="text/html; charset=utf-8")
                except ParkingMarker.DoesNotExist:
                    register_error(12)
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

@csrf_exempt
def actualise_available_spaces(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.method == "POST":
                available_spaces = request.POST['available_spaces']
                try:
                    parking_id = Client.objects.get(user=request.user.id).parking_id
                    ParkingMarker.objects.filter(id=parking_id).update(availableSpaces=available_spaces)
                except Client.DoesNotExist:
                    register_error(13)
                    return HttpResponse("Client does not exist", content_type="text/html; charset=utf-8")
                return HttpResponse("actualising available spaces complete", content_type="text/html; charset=utf-8")        
            else:
                return HttpResponse("request method is not POST", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("user not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")
   
def test_error_messages(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.user.id == 1:
                for i in range(1,15):
                    register_error(i)
                return HttpResponse("test complete", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("not admin", content_type="text/html; charset=utf-8")
        else:
            return HttpResponse("User not authenticated", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")