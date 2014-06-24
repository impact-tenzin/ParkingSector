from django.shortcuts import render_to_response
from django.template import RequestContext
from useful.models import UsefulInformation
from django.contrib.sites.models import Site

def loadInfo(request):  
    """
    returns html with dropdown for the user to choose city he/she is interested in  
    """
    context = {'domain':Site.objects.get_current().domain }
    return render_to_response('useful.html', context, context_instance=RequestContext(request))

def loadInfoForCity(request, city):
    """
    depending on which city the user has selected a proper template with info for the city is returned
    """
    #has to be completed in such way to serve info for different cities
    blueZone = UsefulInformation.objects.get(title="blueZone")
    greenZone = UsefulInformation.objects.get(title="greenZone")
    finesInfo = UsefulInformation.objects.get(title="finesInfo")
    notificationsInfo = UsefulInformation.objects.get(title="notificationsInfo")
    context = {'blueZone': blueZone, 'greenZone': greenZone, 'finesInfo': finesInfo,
               'notificationsInfo': notificationsInfo, 'selectedCity':city, 'domain':Site.objects.get_current().domain }
    return render_to_response('sofia.html', context, context_instance=RequestContext(request))
    
