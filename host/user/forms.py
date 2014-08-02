from django import forms
from django.contrib.auth.models import User
from user.models import RegularUser

class RegistrationForm(forms.Form):
    username = forms.CharField()    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False))        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
        