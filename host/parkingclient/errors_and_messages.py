import datetime
from django.core.mail import EmailMessage
from parkingclient.models import ErrorHistory

def register_error(number):
    if number == 1:
       description = bookedspot_does_not_exist()
    elif number == 2:
       pass
    elif number == 3:
       pass
    else:
       pass
    send_error_email(description)

def send_error_email(description):
    date_time = "datetime: "+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    description = date_time + description
    ErrorHistory.objects.create(description=description).save()
    email = EmailMessage('PS Error', description, to=['mihail_workbuz@abv.bg'])
    email.send()

def bookedspot_does_not_exist():
    description = """
        function:  save_parking_info
        fragment:
                try:
                    spot = BookedSpots.objects.get(id=request.POST['booking_id'])
                except BookedSpots.DoesNotExist:
                    register_error(1)
        """
    return description