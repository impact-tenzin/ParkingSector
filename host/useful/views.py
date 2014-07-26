# -*- coding: utf-8 -*- 
from django.shortcuts import render_to_response
from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from FindParking.models import ParkingMarker
from django.core import serializers
import pusher
#from django_pusher.push import pusher

pusher.app_id = settings.PUSHER_APP_ID
pusher.key = settings.PUSHER_KEY
pusher.secret = settings.PUSHER_SECRET

p = pusher.Pusher()

def add_socket_id(request):
    #socket_ids[request.session['user']] = request.POST.get("socket_id")
    return HttpResponse('')

def home(request):
    if not request.session.get('user'):
        request.session['user'] = 'user-%s' % request.session.session_key
    return render_to_response('home.html', {
        'PUSHER_KEY': settings.PUSHER_KEY,
    }, RequestContext(request)) 

def message(request):
    parkings = ParkingMarker.objects.filter(city__exact='София')
    data = serializers.serialize("json", parkings)
    if request.session.get('user') and request.POST.get('message'):
        p['chat'].trigger('message', {
            'message': request.POST.get('message'),
            'user': request.session['user'],
            'parkings': data,
            'socketid' : request.POST.get('socketid'),
        }, request.POST.get('socketid'))
    return HttpResponse('')