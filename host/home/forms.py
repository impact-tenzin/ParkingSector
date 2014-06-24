from django import forms

class LocationForm(forms.Form):
    """
    form containing fields for lat/lng coordinates,address and calendar
    """
    address = forms.CharField(required=False)
    lat = forms.FloatField()
    lng = forms.FloatField()
    
class SubscribeForm(forms.Form):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=False)
    #is_parkingowner = forms.BooleanField(required=False)
