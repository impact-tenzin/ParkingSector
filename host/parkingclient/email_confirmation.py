from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

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
    msg.send()