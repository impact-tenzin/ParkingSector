from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.MIMEImage import MIMEImage
import os

def send_confirmation_email(id, booked):
    email = User.objects.get(id=id).email
    #description = "Thank you for using our services!" + booked.parking_address + booked.arrival_time + booked.licence_plate
    #EmailMessage('Booking confirmation', description, to=[email]).send()
    
    template_html = 'email_confirmation.html'
    template_text = 'email_confirmation.txt'

    subject = "Booking confirmation"

    from_email = settings.DEFAULT_FROM_EMAIL           

    text_content = render_to_string(template_text, {"booked": booked})
    html_content = render_to_string(template_html, {"booked": booked})

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