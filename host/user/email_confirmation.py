from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.MIMEImage import MIMEImage
import os
import datetime
from django.contrib.sites.models import Site
from client.errors_and_messages import register_error
from user.forms import LoginForm

def send_confirmation_email(id, booked):
    email = User.objects.get(id=id).email
    #description = "Thank you for using our services!" + booked.parking_address + booked.arrival_time + booked.licence_plate
    #EmailMessage('Booking confirmation', description, to=[email]).send()
    
    template_html = 'email_confirmation.html'
    template_text = 'email_confirmation.txt'

    subject = "Booking confirmation"

    from_email = settings.DEFAULT_FROM_EMAIL           
    date = str(datetime.datetime.now().strftime("%d %B"))
    
    text_content = render_to_string(template_text, {"booked": booked, "date":date})
    html_content = render_to_string(template_html, {"booked": booked, "date":date})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    
    #images = ['checkmark_big.png']
    
    #for image in images:
        #fp = open('/home/park0odf/www.testparkingsector.bg/static/imgs/mail/' + image, 'rb')
        #msg_img = MIMEImage(fp.read())
        #fp.close()
        #msg_img.add_header('Content-ID', '<{0}>'.format(image))
        #msg.attach(msg_img)
    
    msg.send()
    
def send_account_activation_email(email, activation_key, user_id):
    template_html = 'email_acc_activation.html'
    template_text = 'email_acc_activation.txt'

    subject = "ParkingSector account activation"

    from_email = settings.DEFAULT_FROM_EMAIL           
    date = str(datetime.datetime.now().strftime("%d %B"))
    
    current_site = Site.objects.get_current().domain
    activation_url = content = "http://" + current_site + "/confirm/" + activation_key + "/" + user_id
    
    text_content = render_to_string(template_text, {"activation_url": activation_url, "date":date})
    html_content = render_to_string(template_html, {"activation_url": activation_url, "date":date})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    
    #images = ['checkmark_big.png']
    
    #for image in images:
        #fp = open('/home/park0odf/www.testparkingsector.bg/static/imgs/mail/' + image, 'rb')
        #msg_img = MIMEImage(fp.read())
        #fp.close()
        #msg_img.add_header('Content-ID', '<{0}>'.format(image))
        #msg.attach(msg_img)
    
    msg.send()
    
def confirm(request, activation_key, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        HttpResponseRedirect('/error_page/')
        register_error(16)
    
    try:
        profile = UserProfile.objects.get(user=user)
        if profile.activation_key == activation_key:# and user.date_joined > (datetime.datetime.now()-datetime.timedelta(days=1)):
            user.is_active = True
            user.save()
            #user.backend='django.contrib.auth.backends.ModelBackend' 
            #auth_login(request,user)
            return redirect_to_login(request)
        else:
            register_error(17)
            return HttpResponseRedirect('/error_page/')
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/error_page/')
        register_error(18)
    except:
        HttpResponseRedirect('/error_page/')
        register_error(19)

def redirect_to_login():
    form = LoginForm()
    return render_to_response('loginuser.html',
                                {'form': form, 'msg-confirm':'Успешно активирахте вашия акаунт в ParkingSector.'},
                                  context_instance=RequestContext(request)) 