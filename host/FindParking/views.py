# -*- coding: utf-8 -*- 
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse
from home.forms import LocationForm, SubscribeForm
from FindParking.models import ParkingMarker, ParkingFeatures, PaymentMethod, PriceList
from home.views import distance
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from home.models import Viewer
from django.core import serializers
from itertools import chain

def find_parking(request):  
    """
    function that take a request from the website
    and if request is GET then returns html with a form containing base values for 
    some fields: fromHour, toHour, fromPeriod, toPeriod;
    if POST then takes the latitude and longitude coordinates of the address that the user has written
    as well as the address, then make SQL requests for near parkings and their features
    finally returns html with selected parkings 
    """
    if request.method == 'GET':
        return render_map_with_default_parkings(request)
    else:        return render_to_response('findparking.html', context, context_instance=RequestContext(request))        """
        try:
            subscribe_form = SubscribeForm(request.POST);
            address_form = LocationForm()
            if subscribe_form.is_valid():
                email = subscribe_form.cleaned_data['email']
                name = subscribe_form.cleaned_data['name']
                to_add = Viewer.objects.create(email = email, name = name)
                to_add.save()
                context = {'msg':'thanks','form':'subscribeForm', 'addressForm':address_form,'subscribeForm':subscribe_form,}
                return render_to_response('index.html', context, context_instance=RequestContext(request))
            context = {'msg':'notValid','form':'subscribeForm', 'addressForm':address_form,'subscribeForm':subscribe_form,}
            return render_to_response('findparking.html', context, context_instance=RequestContext(request))
        except IntegrityError:
            context = {'msg':'existing','form':'subscribeForm','addressForm':address_form,'subscribeForm':subscribe_form,}
            return render_to_response('findparking.html', context, context_instance=RequestContext(request))        """
        """
        address_form = LocationForm(request.POST)
        if address_form.is_valid():
            address_lat = address_form.cleaned_data['lat']
            address_lng = address_form.cleaned_data['lng']
            parkings = [parking for parking in ParkingMarker.objects.all() if distance([parking.lat, parking.lng], [address_lat, address_lng]) < 1]
            features = [ParkingFeatures.objects.get(id=parking.features_id) for parking in parkings]
            payment_methods = [PaymentMethod.objects.get(id=parking.paymentMethod_id) for parking in parkings]
            context = {'addressForm':address_form, 'parkings':parkings, 'features':features, 'paymentMethods':payment_methods,
                             'lat':address_lat, 'lng':address_lng,}
            return render_to_response('findparking.html', context , context_instance=RequestContext(request))
        else:
            return render_to_response('findparking.html', {'addressForm':address_form,} , context_instance=RequestContext(request))
        """
def render_map_with_default_parkings(request):        address_form = LocationForm()        address_lat = 42.697838        address_lng = 23.321669        context = {                   'addressForm':address_form,                    'loadDefaultParkings':"defaultSofia",                    'lat':address_lat,                    'lng':address_lng                    }        return render_to_response('findparking.html', context, context_instance=RequestContext(request))
@csrf_exempt     
def ajax_call(request, latlng):
    if request.is_ajax():
        lat = float(latlng.split('/')[0])
        lng = float(latlng.split('/')[1])        
        parkings = [parking                    for parking in ParkingMarker.objects.all()
                    if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5        ]
        methods = [PaymentMethod.objects.get(id=parking.paymentMethod_id)                   for parking in ParkingMarker.objects.all() 
                   if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5        ]
        features = [ParkingFeatures.objects.get(id=parking.features_id)                    for parking in ParkingMarker.objects.all() 
                    if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5        ]
                price_lists = [PriceList.objects.get(id=parking.priceList_id)                    for parking in ParkingMarker.objects.all()                     if distance([parking.lat, parking.lng], [float(lat), float(lng)]) < 0.5        ]                combined = list(chain(parkings, methods, features, price_lists))
        data = serializers.serialize("json", combined)
        return HttpResponse(data, content_type="application/json; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def sofia_parkings(request):
    if request.is_ajax():
        parkings = ParkingMarker.objects.filter(city__exact='София')
        features = [ParkingFeatures.objects.get(id=parking.features_id)                    for parking in parkings        ]
        payment_methods = [PaymentMethod.objects.get(id=parking.paymentMethod_id)                           for parking in parkings        ]                price_lists = [PriceList.objects.get(id=parking.priceList_id)                           for parking in parkings        ]
        combined = list(chain(parkings, payment_methods, features, price_lists))
        data = serializers.serialize("json", combined)
        return HttpResponse(data, content_type="application/json; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")

def mark_booking(request):
    if request.is_ajax():
        parking_id = request.POST['id']
        current_counter = int(ParkingMarker.objects.get(id=parking_id).bookingCounter)
        current_counter = current_counter + 1
        ParkingMarker.objects.filter(id=parking_id).update(bookingCounter=current_counter)
        return HttpResponse("Completed", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")
    
def save_viewer(request):
    if request.is_ajax():
        try:
            email = request.POST['email']
            name = request.POST['name']
            to_add = Viewer.objects.create(email=email, name=name)
            to_add.save()
            return HttpResponse("thanks", content_type="text/html; charset=utf-8")
        except IntegrityError:
            return HttpResponse("existing", content_type="text/html; charset=utf-8")
    else:
        return HttpResponse("Error", content_type="text/html; charset=utf-8")
